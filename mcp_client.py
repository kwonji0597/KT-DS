# MCP (Model Context Protocol)를 사용해서 수학 서버와 연동하는 LangGraph 에이전트를 만드는 코드
# 주요 구성 요소:
# MCP 서버 연결: math_server.py와 stdio로 통신
# 도구 로딩: MCP 서버에서 제공하는 tool(도구)들을 가져옴
# 에이전트 생성: OpenAI GPT-4.1-mini + 도구들로 ReAct 에이전트 구성
# 수학 계산 실행: "(3 + 5) x 12?" 질문 처리

from dotenv import load_dotenv
import asyncio  # 이 줄이 빠져있었어요!

load_dotenv()

# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

server_params = StdioServerParameters(
    command="python",
    # Make sure to update to the full absolute path to your math_server.py file
    # args=["C:\Users\User\kt-ds\math_server.py"], # math_server 서버경로
    # args=[r"C:\Users\User\kt-ds\math_server.py"],
    # 수정 방법 1: raw string 사용 (추천)
args=[r"C:\Users\User\kt-ds\math_server.py"], # math_server 서버경로
)


# 비동기 함수로 감싸기 - #내가 추가한 부분
async def main():

    # 클라이언트는 비동기 방식으로 기동되어야 함
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent("openai:gpt-4.1-mini", tools) # 랭그래프에서 만드는 에이젼트 제공 (도구와 llm전달후 에이전트 )
            agent_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})  # 도구 호출

    print(agent_response)




# 실행 - #내가 추가한 부분
if __name__ == "__main__":
    asyncio.run(main())