from main import run_crew

if __name__ == "__main__":
    print("Starting CrewAI process...")
    # Using the generated data/sample.pdf
    result = run_crew("What are the key takeaways from this financial document?", "data/sample.pdf")
    print("\n--- FINAL ANALYSIS RESULT ---\n")
    print(result)
