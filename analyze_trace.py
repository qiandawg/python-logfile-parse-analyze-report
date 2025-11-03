import sys

def analyze_memory_trace(log_file):
    """
    Parses a server trace log and calculates key performance metrics.
    """
    
    # These dictionaries and lists will store our counters
    stats = {
        "CACHE_HIT": 0,
        "CACHE_MISS": 0,
        "TLB_HIT": 0,
        "TLB_MISS": 0,
    }
    memory_latencies = []
    
    print(f"--- Starting analysis of {log_file} ---")

    try:
        with open(log_file, 'r') as f:
            for line_number, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue  # Skip empty lines

                # Split the line into its main parts: TIMESTAMP::EVENT::DETAILS
                parts = line.split('::')
                if len(parts) != 3:
                    print(f"Warning: Skipping malformed line {line_number + 1}: {line}")
                    continue
                
                event_type = parts[1]
                details_str = parts[2]
                
                # Parse the "key=value,key=value" details into a Python dictionary
                details_map = {}
                try:
                    for item in details_str.split(','):
                        key, value = item.split('=')
                        details_map[key] = value
                except ValueError:
                    print(f"Warning: Skipping malformed details on line {line_number + 1}: {details_str}")
                    continue
                
                # --- This is the main logic ---
                # Increment the correct counter based on the event type
                
                if event_type == 'CACHE_ACCESS':
                    if details_map.get('status') == 'HIT':
                        stats['CACHE_HIT'] += 1
                    elif details_map.get('status') == 'MISS':
                        stats['CACHE_MISS'] += 1
                        
                elif event_type == 'TLB_LOOKUP':
                    if details_map.get('status') == 'HIT':
                        stats['TLB_HIT'] += 1
                    elif details_map.get('status') == 'MISS':
                        stats['TLB_MISS'] += 1
                        
                elif event_type == 'MEM_READ':
                    # For latencies, we append them to a list to average later
                    memory_latencies.append(int(details_map.get('latency_ns', 0)))

    except FileNotFoundError:
        print(f"Error: Log file not found at {log_file}")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # --- Generate the final report ---
    print("\n--- 📈 Performance Analysis Report ---")

    # 1. Cache Performance
    total_cache_accesses = stats['CACHE_HIT'] + stats['CACHE_MISS']
    if total_cache_accesses > 0:
        hit_rate = (stats['CACHE_HIT'] / total_cache_accesses) * 100
        print("\n## Cache Performance")
        print(f"  Total Accesses: {total_cache_accesses}")
        print(f"  Cache Hits:     {stats['CACHE_HIT']}")
        print(f"  Cache Misses:   {stats['CACHE_MISS']}")
        print(f"  Cache Hit Rate: {hit_rate:.2f}%")
    else:
        print("\n## No Cache data found.")

    # 2. TLB Performance
    total_tlb_lookups = stats['TLB_HIT'] + stats['TLB_MISS']
    if total_tlb_lookups > 0:
        tlb_hit_rate = (stats['TLB_HIT'] / total_tlb_lookups) * 100
        print("\n## TLB Performance")
        print(f"  Total Lookups: {total_tlb_lookups}")
        print(f"  TLB Hits:      {stats['TLB_HIT']}")
        print(f"  TLB Misses:    {stats['TLB_MISS']}")
        print(f"  TLB Hit Rate:  {tlb_hit_rate:.2f}%")
    else:
        print("\n## No TLB data found.")

    # 3. Memory Latency
    if memory_latencies:
        avg_latency = sum(memory_latencies) / len(memory_latencies)
        print("\n## Memory Subsystem")
        print(f"  Total DRAM Reads:  {len(memory_latencies)}")
        print(f"  Average Latency: {avg_latency:.2f} ns")
    else:
        print("\n## No Memory Read data found.")


# --- Script entry point ---
if __name__ == "__main__":
    # This makes the script take the log file name as an argument
    # e.g., python analyze_trace.py epyc_trace.log
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        # Or default to this name if none is given
        filename = 'epyc_trace.log'
        
    analyze_memory_trace(filename)