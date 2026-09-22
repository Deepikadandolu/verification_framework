module alu_tb;
    parameter DUT_MODULE = "alu";
    reg clk=0; always #5 clk=~clk;
    reg rst_n=0, valid=0, ready=0;
    reg [31:0] a=0,b=0; reg [2:0] op=0;
    wire out_valid; wire [31:0] y;

    // The runner substitutes the DUT source/module by generating this wrapper at runtime.
    alu dut(.clk(clk),.rst_n(rst_n),.valid(valid),.ready(ready),.a(a),.b(b),.op(op),.out_valid(out_valid),.y(y));

    integer in_f, out_f;
    integer id;
    integer cycle_count;
    reg [31:0] prev_a, prev_b; reg [2:0] prev_op; reg prev_valid, prev_ready;

    always @(posedge clk) begin
        cycle_count <= cycle_count + 1;
        // Protocol monitor: if a transaction is stalled, inputs must remain stable.
        if (rst_n && prev_valid && !prev_ready) begin
            if (a !== prev_a || b !== prev_b || op !== prev_op)
                $display("ASSERT_FAIL|cycle=%0d|type=STABLE_WHILE_STALLED", cycle_count);
        end
        prev_a <= a; prev_b <= b; prev_op <= op;
        prev_valid <= valid; prev_ready <= ready;
        if (rst_n && out_valid) begin
            $fwrite(out_f, "%0d,%0d,%h\n", id, cycle_count, y);
        end
    end

    initial begin
        cycle_count=0; id=-1;
        in_f=$fopen("vectors.txt","r");
        out_f=$fopen("rtl_results.txt","w");
        if (!in_f || !out_f) $fatal(1,"Could not open vector/result file");
        #20; rst_n=1; ready=1;
        while (!$feof(in_f)) begin
            if ($fscanf(in_f,"%d %d %h %h", id, op, a, b) == 4) begin
                valid=1; @(posedge clk); #1; valid=0; @(posedge clk); #1;
            end else begin
                @(posedge clk);
            end
        end
        #20; $fclose(in_f); $fclose(out_f); $finish;
    end
endmodule
