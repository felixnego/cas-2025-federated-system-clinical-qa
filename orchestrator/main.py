import asyncio
from agent import aggregate_results
from summarize import generate_summary


def main():
    query = input("🩺 Enter a clinical question: ")
    top_k = 5

    print("\n🔍 Searching hospitals...")
    results = asyncio.run(aggregate_results(query, top_k))

    print(f"\n✅ Retrieved {len(results)} relevant entries:")
    for r in results:
        print(f"  [{r['source']}] Score: {r['score']:.2f} | Time: {r['time']}")

    print("\n🧠 Generating final answer...\n")
    summary = generate_summary(query, results)
    print("💬 Final answer:")
    print(summary)

if __name__ == "__main__":
    main()
