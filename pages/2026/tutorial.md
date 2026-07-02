# Tutorials

Show times in: <timeselector>

From <time Thursday 15:00> on Thursday 9 July, there will be a tutorial session.
During this session, there are a number of tutorials running in parallel for you to choose
from. The list of tutorials is given below.

<h2 style='margin-bottom:0px'>A beginner's guide to Rust</h2>
<div>
<div class='authors'><b>Ignacia Fierro Piccardo</b> (University of Bath)</div>
<div class='authors'><b>Matthew Scroggs</b> <a href='https://mscroggs.co.uk' class='falink'><i class='fa-brands fa-internet-explorer'></i></a> <a href='mailto:rust@mscroggs.co.uk' class='falink'><i class='fa-solid fa-envelope'></i></a> <a href='https://github.com/mscroggs' class='falink'><i class='fa-brands fa-github'></i></a> <a href='https://mathstodon.xyz/@mscroggs'><i class='fa-brands fa-mastodon'></i></a> (University College London)</div>
</div>

This session is aimed at people who don't use Rust yet, but are attending the workshop as they
are interested in starting to use it. We will cover basic syntax in Rust and a few of the language's
nicest features.

Before this session, please install Rust on your computer. There are instructions for doing
this at [rust-lang.org/tools/install](https://www.rust-lang.org/tools/install).

<h2 style='margin-bottom:0px'>Scientific computing with rustc</h2>
<div>
<div class='authors'><b>Manuel Drehwald</b> <a href='mailto:manuel.drehwald@utoronto.ca' class='falink'><i class='fa-solid fa-envelope'></i></a> <a href='https://github.com/ZuseZ4' class='falink'><i class='fa-brands fa-github'></i></a> (University of Toronto)</div>
</div>

This session will guide the audience through the use of autodiff and gpu offloading in Rust.

As of a few weeks ago, we ship all needed dependencies for `std::autodiff` via rustup and nightly, so installation now takes ~5 seconds! A <a href='https://summerofcode.withgoogle.com/'>GSoC</a> contributor
is also working on adding rustup distribution for `std::offload` (gpu programming). Both these feature will be covered in this tutorial.0

<h2 style='margin-bottom:0px'>Linear algebra in Rust with RLST</h2>
<div>
<div class='authors'><b>Timo Betcke</b> (University College London)</div>
<div>

RLST (the Rust Linear Solver Toolbox) is a Rust linear algebra library that contains a number of data-structures, algorithms, and interfaces
to external solvers.

In this tutorial, we will learn how to use many of the features of RLST with a focus on distributed arrays.

<h2 style='margin-bottom:0px'>3D Scene Inference in ModPPL</h2>
<div>
<div class='authors'><b>Austin Garrett</b> <a href='https://austingarrett.dev' class='falink'><i class='fa-brands fa-internet-explorer'></i></a> <a href='mailto:ajg@purdue.edu' class='falink'><i class='fa-solid fa-envelope'></i></a> <a href='https://github.com/agarret7' class='falink'><i class='fa-brands fa-github'></i></a> (Purdue University)</div>
<div>

This guided, hands-on tutorial introduces probabilistic programming through the lens of inverse graphics: the computer-vision paradigm of inferring the 3D scene that produced an image. Participants will combine a rendering-based generative scene model with user-space MCMC inference, written in ModPPL, to recover structured 3D scene hypotheses directly from images, and will visualize how inference converges on a scene. The tutorial emphasizes ModPPL's programmable inference: how custom proposals and block structure change inference quality and convergence rate.

If you plan to attend this tutorial, please install and verify the following before the session:

- Rust toolchain (stable, via [rustup](https://rustup.rs/)). The tutorial is written in Rust (edition 2021).
- ffmpeg on your `PATH`, used to render the inference-convergence videos. Verify with `ffmpeg -version`.
- Git, to clone the tutorial repository.
- Pre-build the project ahead of time** so crates are downloaded and compiled in advance:
  ```
  git clone https://github.com/agarret7/modppl-derender
  cd modppl-derender
  cargo test --no-run
  ```
  (This fetches `modppl`, `glam`, etc. and warms the build cache. If it completes without error, you're ready.)
- Any video player capable of MP4 playback, to view the rendered convergence videos, for example [VLC](https://www.videolan.org/).
