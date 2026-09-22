module alu (
    input  logic        clk,
    input  logic        rst_n,
    input  logic        valid,
    input  logic        ready,
    input  logic [31:0] a,
    input  logic [31:0] b,
    input  logic [2:0]  op,
    output logic        out_valid,
    output logic [31:0] y
);
    localparam OP_ADD = 3'd0;
    localparam OP_SUB = 3'd1;
    localparam OP_AND = 3'd2;
    localparam OP_OR  = 3'd3;
    localparam OP_XOR = 3'd4;
    localparam OP_SLT = 3'd5;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            out_valid <= 1'b0;
            y <= 32'b0;
        end else begin
            out_valid <= 1'b0;
            if (valid && ready) begin
                case (op)
                    OP_ADD: y <= a + b;
                    OP_SUB: y <= a - b;
                    OP_AND: y <= a & b;
                    OP_OR : y <= a | b;
                    OP_XOR: y <= a ^ b;
                    OP_SLT: y <= ($signed(a) < $signed(b)) ? 32'd1 : 32'd0;
                    default: y <= 32'hDEAD_BEEF;
                endcase
                out_valid <= 1'b1;
            end
        end
    end
endmodule
