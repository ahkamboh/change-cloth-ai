# Change-cloth-AI 🐨

A virtual try-on system that uses AI to visualize how different clothing items would look on a person.

## Overview

Change-cloth-AI is an AI-powered virtual try-on system that allows users to:
- Upload a photo of a person (model image)
- Upload a photo of a clothing item
- Generate realistic visualizations of how the clothing would look on the person

## Features

- **Easy-to-use Interface**: Simple upload system for both model and garment images
- **Pre-loaded Examples**: Includes sample model and garment images for quick testing
- **Customizable Generation**: Adjust parameters like:
  - Number of samples
  - Number of steps
  - Image scale
  - Random seed

## How to Use

1. **Select or Upload Model Image**
   - Choose from provided example models
   - Or upload your own model image (person wearing clothes)

2. **Select or Upload Garment**
   - Choose from provided example garments
   - Or upload your own garment image

3. **Adjust Parameters (Optional)**
   - Steps: Higher values give better quality but take longer
   - Scale: Affects how closely the output follows the input
   - Seed: Set for reproducible results

4. **Generate Output**
   - Click "Generate Outfit" to create the visualization
   - Wait for processing (may take a few moments)

## Technical Details

- Built using Gradio interface
- Powered by diffusion models
- SDK Version: 5.4.0
- Runs on Hugging Face Spaces

## API Usage

You can interact with this model using different APIs. Here are three different implementation options:

### 1. OOTDiffusion API
```python
from gradio_client import Client, handle_file

client = Client("levihsu/OOTDiffusion")
result = client.predict(
    vton_img=handle_file('path_to_model_image.png'),
    garm_img=handle_file('path_to_garment_image.jpg'),
    n_samples=1,
    n_steps=20,
    image_scale=2,
    seed=-1,
    api_name="/process_hd"
)
```

### 2. OutfitAnyone API
```python
from gradio_client import Client, handle_file

client = Client("HumanAIGC/OutfitAnyone")
result = client.predict(
    model_name=handle_file('path_to_model_image.png'),
    garment1=handle_file('path_to_top_garment.png'),
    garment2=handle_file('path_to_bottom_garment.png'),
    api_name="/get_tryon_result"
)
```

### 3. Change-Clothes-AI API
```python
from gradio_client import Client, handle_file

client = Client("jallenjia/Change-Clothes-AI")
result = client.predict(
    dict={"background": handle_file('path_to_image.png'), "layers": [], "composite": None},
    garm_img=handle_file('path_to_garment.png'),
    garment_des="Description",
    is_checked=True,
    is_checked_crop=False,
    denoise_steps=30,
    seed=-1,
    category="upper_body",
    api_name="/tryon"
)
```

### JavaScript Implementation
```javascript
import { Client } from "@gradio/client";

const client = await Client.connect("levihsu/OOTDiffusion");
const result = await client.predict("/process_hd", { 
    vton_img: modelImage, 
    garm_img: garmentImage,     
    n_samples: 1,     
    n_steps: 20,     
    image_scale: 1,     
    seed: -1, 
});
```

### Installation Requirements

For Python:
```bash
pip install gradio_client
```

For JavaScript:
```bash
npm i -D @gradio/client
```

### API Parameters

#### OOTDiffusion Parameters:
- `vton_img`: Model image (person wearing clothes)
- `garm_img`: Garment image
- `n_samples`: Number of samples to generate (default: 1)
- `n_steps`: Number of denoising steps (default: 20)
- `image_scale`: Guidance scale (default: 2)
- `seed`: Random seed (-1 for random)

#### OutfitAnyone Parameters:
- `model_name`: Model image
- `garment1`: Top garment image
- `garment2`: Bottom garment image

#### Change-Clothes-AI Parameters:
- `dict`: Background and layers information
- `garm_img`: Garment image
- `garment_des`: Garment description
- `denoise_steps`: Number of denoising steps
- `category`: Garment category (upper_body, lower_body, dresses)

## Limitations

- Processing time depends on server load
- Free tier has usage quotas
- Best results with clear, front-facing photos
- Garment images should be on white/clear backgrounds

## Tips for Best Results

1. Use clear, well-lit photographs
2. Model should be in a natural, front-facing pose
3. Garment images should be isolated on clean backgrounds
4. Start with lower step counts (10-15) for quick tests
5. Increase steps for final, higher-quality results

## Error Handling

If you encounter quota errors:
- Wait a few minutes between attempts
- Try reducing the number of steps
- Consider signing up for a Hugging Face account for more quota

## Author

**Ali Hamza Kamboh (AHKamBoh)**
- LinkedIn: [Ali Hamza Kamboh](https://www.linkedin.com/in/ahkamboh/)

## Credits

This project uses the Hugging Face Spaces infrastructure and is built on top of state-of-the-art diffusion models for virtual try-on applications.



