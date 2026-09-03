import gradio as gr
from dotenv import load_dotenv

from orchestrator import run_research

load_dotenv(override=True)

CUSTOM_CSS = """
.gradio-container {
    max-width: 820px !important;
    margin: 0 auto !important;
}
#header {
    text-align: center;
    margin-bottom: 0.5rem;
}
#header h1 {
    font-size: 2.1rem;
    font-weight: 700;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.25rem;
}
#header p {
    color: var(--body-text-color-subdued);
    font-size: 1rem;
}
#query-box textarea {
    font-size: 1.05rem !important;
}
#run-btn {
    background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
}
#run-btn:hover {
    opacity: 0.9;
}
#report-card {
    border: 1px solid var(--border-color-primary);
    border-radius: var(--radius-lg);
    padding: 1.25rem;
    background: var(--background-fill-secondary);
}
"""

THEME = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="purple",
    neutral_hue="slate",
)


async def research(query: str) -> str:
    if not query or not query.strip():
        return "Please enter a query."

    report = await run_research(query)

    answer = report.answer
    if report.sources:
        sources = "\n".join(f"- {source}" for source in report.sources)
        answer += f"\n\n**Sources:**\n{sources}"

    return answer


with gr.Blocks(theme=THEME, css=CUSTOM_CSS, title="Deep Research Agent") as demo:
    with gr.Column(elem_id="header"):
        gr.Markdown("# 🔎 Deep Research Agent")
        gr.Markdown("Ask a question and the agent will plan searches, gather findings, and write a report.")

    query_box = gr.Textbox(
        label="Research query",
        placeholder="What do you want to research?",
        lines=2,
        elem_id="query-box",
    )
    run_btn = gr.Button("Research", elem_id="run-btn", variant="primary")

    with gr.Column(elem_id="report-card"):
        report_output = gr.Markdown(label="Report", value="Your report will appear here.")

    run_btn.click(fn=research, inputs=query_box, outputs=report_output)
    query_box.submit(fn=research, inputs=query_box, outputs=report_output)

if __name__ == "__main__":
    demo.launch()
