`include "alu.s"
module alu_fault_stuck1 (
    input logic clk, rst_n, valid, ready,
    input logic [31:0] a, b, input logic [2:0] op,
    output logic out_valid, output logic [31:0] y
);
    logic [31:0] golden_y;
    alu u(.clk(clk),.rst_n(rst_n),.valid(valid),.ready(ready),.a(a),.b(b),.op(op),.out_valid(out_valid),.y(golden_y));
    always_comb y = {golden_y[31:1],1'b1};
endmodule
