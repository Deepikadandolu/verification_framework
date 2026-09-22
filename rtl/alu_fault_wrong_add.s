`include "alu.s"
module alu_fault_wrong_add (
    input logic clk, rst_n, valid, ready,
    input logic [31:0] a, b, input logic [2:0] op,
    output logic out_valid, output logic [31:0] y
);
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin out_valid <= 0; y <= 0; end
        else begin
            out_valid <= 0;
            if (valid && ready) begin
                case (op)
                    3'd0: y <= a - b; // MUTATION: ADD -> SUB
                    3'd1: y <= a - b;
                    3'd2: y <= a & b;
                    3'd3: y <= a | b;
                    3'd4: y <= a ^ b;
                    3'd5: y <= ($signed(a) < $signed(b)) ? 32'd1 : 32'd0;
                    default: y <= 32'hDEAD_BEEF;
                endcase
                out_valid <= 1;
            end
        end
    end
endmodule
