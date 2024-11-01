import gradio as gr
from gradio_client import Client, handle_file
import re
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Hugging Face token from environment variable
hf_token = os.getenv("HUGGING_FACE_HUB_TOKEN")

# Initialize client with auth
client = Client(
    "levihsu/OOTDiffusion",
    hf_token=hf_token
)


def generate_outfit(model_image, garment_image, n_samples=1, n_steps=20, image_scale=2, seed=-1):
    if model_image is None or garment_image is None:
        return None, "Please upload both model and garment images"
        
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Use the client to predict
            result = client.predict(
                vton_img=handle_file(model_image),
                garm_img=handle_file(garment_image),
                n_samples=n_samples,
                n_steps=n_steps,
                image_scale=image_scale,
                seed=seed,
                api_name="/process_hd"
            )
            
            # If result is a list, get the first item
            if isinstance(result, list):
                result = result[0]
            
            # If result is a dictionary, try to get the image path
            if isinstance(result, dict):
                if 'image' in result:
                    return result['image'], None
                else:
                    return None, "API returned unexpected format"
                
            return result, None
            
        except Exception as e:
            error_msg = str(e)
            if "exceeded your GPU quota" in error_msg:
                wait_time_match = re.search(r'retry in (\d+:\d+:\d+)', error_msg)
                wait_time = wait_time_match.group(1) if wait_time_match else "60:00"  # Default to 1 hour
                wait_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(wait_time.split(':'))))  # Convert wait time to seconds
                if attempt < max_retries - 1:
                    time.sleep(wait_seconds)  # Wait before retrying
                return None, f"GPU quota exceeded. Please wait {wait_time} before trying again."
            else:
                return None, f"Error: {str(e)}"

# Create Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("""
    ## Outfit Diffusion - Try On Virtual Outfits

    ⚠️ **Note**: This demo uses free GPU quota which is limited. To avoid errors:
    - Use lower values for Steps (10-15) and Scale (1-2)
    - Wait between attempts if you get a quota error
    - Sign up for a Hugging Face account for more quota

  
    """)

    with gr.Row():
        with gr.Column():
            model_image = gr.Image(
                label="Upload Model Image (person wearing clothes)", 
                type="filepath",
                height=300
                
            )
            model_examples = [
                "https://levihsu-ootdiffusion.hf.space/file=/tmp/gradio/ba5ba7978e7302e8ab5eb733cc7221394c4e6faf/model_5.png",
                "https://levihsu-ootdiffusion.hf.space/file=/tmp/gradio/40dade4a04a827c0fdf63c6c70b42ef26480f391/01861_00.jpg",
                "https://levihsu-ootdiffusion.hf.space/file=/tmp/gradio/3c4639c5fab3cdcd3239609dca5afee7b0677286/model_6.png",
                "https://levihsu-ootdiffusion.hf.space/file=/tmp/gradio/0089171df270f4532eec3d80a8f36cc8218c6840/01008_00.jpg"
            ]
            gr.Examples(examples=model_examples, inputs=model_image)

            garment_image = gr.Image(
                label="Upload Garment Image (clothing item)", 
                type="filepath",
                height=300
            )
            garment_examples = [
                "https://levihsu-ootdiffusion.hf.space/file=/tmp/gradio/180d4e2a1139071a8685a5edee7ab24bcf1639f5/03244_00.jpg",
                "https://levihsu-ootdiffusion.hf.space/file=/tmp/gradio/584dda2c5ee1d8271a6cd06225c07db89c79ca03/04825_00.jpg",
                "https://levihsu-ootdiffusion.hf.space/file=/tmp/gradio/a51938ec99f13e548d365a9ca6d794b6fe7462af/049949_1.jpg",
                "https://levihsu-ootdiffusion.hf.space/file=/tmp/gradio/2d64241101189251ce415df84dc9205cda9a36ca/03032_00.jpg",
                "https://levihsu-ootdiffusion.hf.space/file=/tmp/gradio/44aee6b576cae51eeb979311306375b56b7e0d8b/02305_00.jpg",
                "https://levihsu-ootdiffusion.hf.space/file=/tmp/gradio/578dfa869dedb649e91eccbe566fc76435bb6bbe/049920_1.jpg"
            ]
            gr.Examples(examples=garment_examples, inputs=garment_image)

        
        with gr.Column():
            output_image = gr.Image(label="Generated Output")
            error_text = gr.Markdown()  # Add error display
    
    with gr.Row():
        with gr.Column():
            n_samples = gr.Slider(
                label="Number of Samples", 
                minimum=1, 
                maximum=5, 
                step=1, 
                value=1
            )
            n_steps = gr.Slider(
                label="Steps (lower = faster, try 10-15)", 
                minimum=1, 
                maximum=50, 
                step=1, 
                value=10  # Reduced default
            )
            image_scale = gr.Slider(
                label="Scale (lower = faster, try 1-2)", 
                minimum=1, 
                maximum=5, 
                step=1, 
                value=1  # Reduced default
            )
            seed = gr.Number(
                label="Random Seed (-1 for random)", 
                value=-1
            )
    
    generate_button = gr.Button("Generate Outfit")

    # Set up the action for the button
    generate_button.click(
        fn=generate_outfit,
        inputs=[model_image, garment_image, n_samples, n_steps, image_scale, seed],
        outputs=[output_image, error_text]
    )

# Launch the app
demo.launch()
