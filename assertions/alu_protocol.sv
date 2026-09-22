// Optional SVA layer for simulators with full SystemVerilog Assertion support.
// The portable procedural checks in tb/alu_tb.sv remain the default for Icarus.
module alu_protocol_sva (
    input logic clk,
    input logic rst_n,
    input logic valid,
    input logic ready,
    input logic [31:0] a,
    input logic [31:0] b,
    input logic [2:0] op,
    input logic out_valid
);
    // A stalled request must keep its transaction fields stable.
    p_stable_when_stalled: assert property (@(posedge clk) disable iff (!rst_n)
        valid && !ready |=> valid && $stable(a) && $stable(b) && $stable(op));

    // Output valid is only legal after a previously accepted request in this
    // one-cycle registered ALU implementation.
    p_output_follows_accept: assert property (@(posedge clk) disable iff (!rst_n)
        out_valid |-> $past(valid && ready));

    // Unknown control/data values are not allowed on accepted transactions.
    p_known_request: assert property (@(posedge clk) disable iff (!rst_n)
        valid && ready |-> !$isunknown({a,b,op}));
endmodule
