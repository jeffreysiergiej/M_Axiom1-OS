from M_Axiom1_Mobile_Core import AxiomCoreEngine

def plot_entropy_history(memory_log, output_path="entropy_plot.png"):
    import matplotlib.pyplot as plt
    entropy_values = []
    timestamps = []

    for entry in memory_log:
        if "Entropy checked" in entry.get("message", ""):
            try:
                value = float(entry["message"].split(":")[-1])
                entropy_values.append(value)
                timestamps.append(entry["time"])
            except:
                continue

    if entropy_values:
        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, entropy_values, marker='o')
        plt.xticks(rotation=45, fontsize=8)
        plt.title("Entropy History")
        plt.xlabel("Time")
        plt.ylabel("Entropy Flux")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        print(f"Entropy graph saved to {output_path}")
    else:
        print("No entropy data found.")

def rotate_memory_log(memory_log, max_entries=1000):
    return memory_log[-max_entries:]

# === Main Launcher ===
if __name__ == "__main__":
    engine = AxiomCoreEngine()
    engine.initialize()

    try:
        with open("axiom_memory_log.json", "r") as f:
            engine.memory_log = rotate_memory_log(json.load(f))
            engine.log("Previous memory log reloaded.")
    except:
        engine.log("No previous memory found.")

    engine.inject_agents()
    engine.trigger_collapse()
    entropy = engine.get_entropy()
    engine.export_memory()
    plot_entropy_history(engine.memory_log)

    print("\n--- AxiomOS Mobile Console ---")
    print("Type commands like: init, inject, collapse, entropy, export")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            cmd = input(">> ").strip().lower()
            if cmd == "exit":
                print("Exiting Axiom Console.")
                break
            elif cmd == "init":
                engine.initialize()
            elif cmd == "inject":
                engine.inject_agents()
            elif cmd == "collapse":
                engine.trigger_collapse()
            elif cmd == "entropy":
                print(engine.get_entropy())
            elif cmd == "export":
                engine.export_memory()
            else:
                print("Unknown command.")
        except KeyboardInterrupt:
            print("\nConsole interrupted.")
            break