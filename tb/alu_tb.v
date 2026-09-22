`timescale 1ns/1ps

module alu_tb;

reg [31:0] a;
reg [31:0] b;
reg [2:0] op;
wire [31:0] y;

integer fd_in;
integer fd_out;
integer rc;
integer a_i;
integer b_i;
integer op_i;

alu dut (
    .a(a),
    .b(b),
    .op(op),
    .y(y)
);

initial begin
    fd_in = $fopen("reports/vectors.txt", "r");
    fd_out = $fopen("reports/rtl_results.txt", "w");

    if (fd_in == 0) begin
        $display("ERROR: could not open reports/vectors.txt");
        $finish;
    end

    if (fd_out == 0) begin
        $display("ERROR: could not open reports/rtl_results.txt");
        $finish;
    end

    while (!$feof(fd_in)) begin
        rc = $fscanf(fd_in, "%d %d %d\n", a_i, b_i, op_i);
        if (rc == 3) begin
            a = a_i[31:0];
            b = b_i[31:0];
            op = op_i[2:0];
            #1;
            $fwrite(fd_out, "%08h\n", y);
        end
    end

    $fclose(fd_in);
    $fclose(fd_out);
    $finish;
end

endmodule
