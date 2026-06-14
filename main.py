from agents.multi_tool_agent import multi_tool_agent


if __name__ == "__main__":
  print("Multi-tool agent is ready. Type 'exit' to stop.")

  while True:
    user_question = input("\nYou: ").strip()
    if user_question.lower() in {"exit", "quit"}:
      break

    answer = multi_tool_agent(user_question)
    print(f"Agent: {answer}")
