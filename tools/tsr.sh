set -x
git clone --depth 1 https://github.com/VAST-AI-Research/TripoSR.git tsr
cd tsr
pip install --quiet torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install --quiet omegaconf==2.3.0 Pillow einops transformers==4.35.0 trimesh rembg[cpu] huggingface-hub imageio[ffmpeg] xatlas moderngl PyMCubes onnxruntime 2>&1 | tail -5
pip install --quiet git+https://github.com/tatsy/torchmcubes.git 2>&1 | tail -3 || true
python -c "import torchmcubes" || sed -i 's/from torchmcubes import marching_cubes/import mcubes\nimport torch\ndef marching_cubes(v,t):\n    a,b=mcubes.marching_cubes(v.detach().cpu().numpy(),t)\n    return torch.from_numpy(a.astype("float32")),torch.from_numpy(b.astype("int64"))/' tsr/models/isosurface.py
python run.py ../in/front.png --output-dir ../out --mc-resolution 320 --foreground-ratio 0.88 --model-save-format obj 2>&1 | tail -20
ls -la ../out ../out/* || true
