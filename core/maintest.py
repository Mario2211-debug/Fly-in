#!/usr/bin/env python3
# main.py
import sys
import argparse
from core.parser import parser
from core.simulation import Simulation


def main():
    parser_args = argparse.ArgumentParser(description="Fly-in Drone Routing System")
    parser_args.add_argument("map_file", help="Path to the map file")
    parser_args.add_argument("--visual", action="store_true", help="Enable visual output")

    args = parser_args.parse_args()

    # Parse map file
    try:
        with open(args.map_file, "r") as f:
            conf = parser(f)
    except Exception as e:
        print(f"Error parsing map: {e}")
        sys.exit(1)

    print(f"Map loaded: {conf.n_drones} drones")
    print(f"Start: {conf.start.name} ({conf.start.x}, {conf.start.y})")
    print(f"End: {conf.end.name} ({conf.end.x}, {conf.end.y})")
    print(f"Hubs: {len(conf.hubs)}")
    print(f"Connections: {len(conf.connections)}")

    # Run simulation
    sim = Simulation(conf)
    output = sim.run()

    # Print results
    print("\n" + "=" * 50)
    print("SIMULATION OUTPUT")
    print("=" * 50)
    for line in output:
        print(line)

    stats = sim.get_stats()
    print("\n" + "=" * 50)
    print(f"STATISTICS")
    print(f"Total turns: {stats['total_turns']}")
    print(f"Drones delivered: {stats['drones_delivered']}/{stats['total_drones']}")
    print("=" * 50)


if __name__ == "__main__":
    main()
