# app.py
import gradio as gr
from backend import (
    get_channel_data,
    get_all_video_categories,
    get_category_name,
    get_channel_id,
    compare_channels,
    suggest_channel_based_on_others,
    calculate_content_frequency,
    get_most_popular_video,
    calculate_engagement_rate,
    rank_channels,
    best_channel
)

# ------------------- Functions to connect UI -------------------

def compare_ui(channel_names):
    handles = [h.strip() for h in channel_names.replace("\n", ",").split(",") if h.strip()]
    if len(handles) < 2:
        return "Please enter at least two channels."
    
    data_list = compare_channels(handles)
    if not data_list:
        return "No valid channel data found."
    
    output = []
    output.append("### Channel Comparison by Subscribers:")
    for i, ch in enumerate(rank_channels(data_list, 'Subscribers'), 1):
        output.append(f"{i}. {ch['Handle']} - {ch['Subscribers']:,} Subscribers")
    
    output.append("\n### Channel Comparison by Views:")
    for i, ch in enumerate(rank_channels(data_list, 'Views'), 1):
        output.append(f"{i}. {ch['Handle']} - {ch['Views']:,} Views")
    
    output.append("\n### Channel Comparison by Engagement Rate:")
    for i, ch in enumerate(rank_channels(data_list, 'Engagement Rate (%)'), 1):
        output.append(f"{i}. {ch['Handle']} - {ch['Engagement Rate (%)']}% Engagement Rate")
    
    output.append("\n### Recommendations:")
    best_engagement = best_channel(data_list, 'Engagement Rate (%)')
    best_views = best_channel(data_list, 'Views')
    output.append(f"Best Channel by Engagement Rate: {best_engagement['Handle']} ({best_engagement['Engagement Rate (%)']}%)")
    output.append(f"Best Channel by Views: {best_views['Handle']} ({best_views['Views']:,} Views)")
    
    return "\n".join(output)

def get_data_ui(channel_names):
    handles = [h.strip() for h in channel_names.replace("\n", ",").split(",") if h.strip()]
    if not handles:
        return "Please enter at least one channel."
    
    output = []
    for handle in handles:
        cid = get_channel_id(handle)
        if not cid:
            output.append(f"Channel '{handle}' not found.")
            continue

        data = get_channel_data(cid)
        if not data:
            output.append(f"No data for {handle}")
            continue

        content_freq = calculate_content_frequency(cid)
        popular_video = get_most_popular_video(cid)

        output.append(f"### Channel: {data['Handle']}")
        output.append(f"Link: {data['Link']}")
        output.append(f"Subscribers: {data['Subscribers']:,}")
        output.append(f"Views: {data['Views']:,}")
        output.append(f"Videos: {data['Videos']:,}")
        output.append(f"Content Frequency: {content_freq if content_freq else 'N/A'} days")
        output.append(f"Most Popular Video: {popular_video if popular_video else 'N/A'}")
        output.append(f"Engagement Rate: {calculate_engagement_rate(data)}%")
        output.append("---")
    
    return "\n".join(output)

def suggest_ui(channel_names):
    handles = [h.strip() for h in channel_names.replace("\n", ",").split(",") if h.strip()]
    if not handles:
        return "Please enter at least one channel."
    
    suggestion = suggest_channel_based_on_others(handles)
    if suggestion:
        return f"Suggested Channel: {suggestion['Handle']} ({suggestion['Link']})"
    return "No similar channels found."

# ------------------- Gradio Interface -------------------

with gr.Blocks() as demo:
    gr.Markdown("## 📊 YouTube Channel Analyzer")
    
    with gr.Tab("Compare Channels"):
        input_compare = gr.Textbox(label="Enter two or more channel names (comma or newline separated)")
        output_compare = gr.Markdown()
        btn_compare = gr.Button("Run Comparison")
        btn_compare.click(compare_ui, inputs=input_compare, outputs=output_compare)
    
    with gr.Tab("Get Channel Data"):
        input_data = gr.Textbox(label="Enter one or more channel names (comma or newline separated)")
        output_data = gr.Markdown()
        btn_data = gr.Button("Get Data")
        btn_data.click(get_data_ui, inputs=input_data, outputs=output_data)
    
    with gr.Tab("Suggest a Channel"):
        input_suggest = gr.Textbox(label="Enter channels you like (comma or newline separated)")
        output_suggest = gr.Markdown()
        btn_suggest = gr.Button("Get Suggestion")
        btn_suggest.click(suggest_ui, inputs=input_suggest, outputs=output_suggest)

demo.launch()
