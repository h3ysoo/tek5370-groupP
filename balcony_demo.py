"""
pandapower demo: 11 kV grid -> 11/0.4 kV transformer -> 400 V street feeder with 10 houses.
Each house has a consumption (load) and optionally a 1.8 kW balcony solar power plant.
We compare voltage and loading in four scenarios, with and without balcony PV.
"""
import pandapower as pp

def build_net():
    net = pp.create_empty_network()

    # 1) Buses (nodes)
    b_mv = pp.create_bus(net, vn_kv=11.0, name="MV bus")
    b_lv0 = pp.create_bus(net, vn_kv=0.4, name="LV busbar")

    # 2) Upstream grid = ideal voltage source (slack bus)
    pp.create_ext_grid(net, bus=b_mv, vm_pu=1.0, name="Grid")

    # 3) Distribution transformer 11/0.4 kV, 250 kVA
    pp.create_transformer_from_parameters(
        net, hv_bus=b_mv, lv_bus=b_lv0, sn_mva=0.25,
        vn_hv_kv=11.0, vn_lv_kv=0.4, vk_percent=4.0, vkr_percent=1.2,
        pfe_kw=0.6, i0_percent=0.3, name="Transformer 11/0.4")

    # 4) Street feeder: 10 houses, 40 m of cable between each house
    prev = b_lv0
    houses = []
    for i in range(10):
        b = pp.create_bus(net, vn_kv=0.4, name=f"House {i+1}")
        pp.create_line(net, from_bus=prev, to_bus=b, length_km=0.04,
                       std_type="NAYY 4x50 SE", name=f"Line {i+1}")
        # Consumption (load) and balcony PV (sgen = static generator)
        pp.create_load(net, bus=b, p_mw=0.0, q_mvar=0.0, name=f"Load {i+1}")
        pp.create_sgen(net, bus=b, p_mw=0.0, name=f"Balcony PV {i+1}")
        houses.append(b)
        prev = b
    return net, houses

scenarios = {
    # name: (load per house [kW], PV per house [kW])
    "Summer noon, low load, max PV":     (0.3, 1.8),
    "Summer, medium load, max PV":       (1.0, 1.8),
    "Winter evening -20C, high load, no PV": (6.0, 0.0),
    "Winter day, high load, little PV":  (5.0, 0.4),
}

net, houses = build_net()

# Reactive power of the loads from a power factor of 0.95 (Q = P * tan(phi))
cos_phi = 0.95
q_factor = (1 / cos_phi**2 - 1) ** 0.5

print(f"{'Scenario':40s} {'U house10 [pu]':>14s} {'U house10 no PV':>16s} "
      f"{'Trafo [%]':>10s} {'P from grid [kW]':>17s}")

for name, (p_load_kw, p_pv_kw) in scenarios.items():
    results = []
    for pv in (p_pv_kw, 0.0):  # run once with and once without balcony PV
        net.load["p_mw"] = p_load_kw / 1000
        net.load["q_mvar"] = p_load_kw / 1000 * q_factor
        net.sgen["p_mw"] = pv / 1000
        pp.runpp(net)  # power flow (Newton-Raphson)
        results.append((net.res_bus.vm_pu.at[houses[-1]],        # voltage at the last house
                        net.res_trafo.loading_percent.at[0],    # transformer loading
                        net.res_ext_grid.p_mw.at[0] * 1000))    # power drawn from the grid
    (u, load_tr, p_grid), (u0, _, _) = results
    # Negative "P from grid" means reverse power flow (local PV exceeds consumption)
    print(f"{name:40s} {u:14.4f} {u0:16.4f} {load_tr:10.1f} {p_grid:17.1f}")
