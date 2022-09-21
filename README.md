## Parallel Bayesian Optimization of Agent-based Transportation Simulation

### [Kiran Chhatre]<sup>1*</sup>, [Sidney Feygin]<sup>2</sup>, [Colin Sheppard]<sup>1,2</sup>, and [Rashid Waraich]<sup>1,2</sup>

<sup>1</sup>[Energy Technologies Area, Berkeley Lab]
<sup>2</sup>[Marain.ai] (now [BrightDrop])

<h4 align="center">
  <a href="https://arxiv.org/abs/2207.05041" target='_blank'>[arXiv]</a> •
  <a href="https://github.com/kiranchhatre/BEAM-Bayes-Opt/wiki" target='_blank'>[Code Wiki]</a> •
  <a href="https://drive.google.com/file/d/1OU0e_WsCJ-k657M2LJUq9lddJMqCeKCd/view?usp=sharing" target='_blank'>[Slides]</a> 
</h4>

![](Docs/beam-structure-med.png?raw=true)
<h4 align="center">
  <a href="https://transportation.lbl.gov/beam/" target='_blank'>Behavior, Energy, Autonomy, and Mobility model</a>
</h4>

[MATSim] (Multi-Agent Transport Simulation Toolkit) is an open source
large-scale agent-based transportation planning project applied to various areas
like road transport, public transport, freight transport, regional evacuation, etc.
[BEAM] (Behavior, Energy, Autonomy, and Mobility) framework extends MAT-
Sim to enable powerful and scalable analysis of urban transportation systems.
The agents from the BEAM simulation exhibit ‘mode choice’ behavior based on
multinomial logit model. In our study, we consider eight mode choices viz. bike,
car, walk, ride hail, driving to transit, walking to transit, ride hail to transit, and
ride hail pooling. The ‘alternative specific constants’ for each mode choice are
critical hyperparameters in a configuration file related to a particular scenario un-
der experimentation. We use the ‘Urbansim-10k’ BEAM scenario (with 10,000
population size) for all our experiments. Since these hyperparameters affect the
simulation in complex ways, manual calibration methods are time consuming.
We present a parallel Bayesian optimization method with early stopping rule to
achieve fast convergence for the given multi-in-multi-out problem to its optimal
configurations. Our model is based on an open source [HpBandSter] package. This
approach combines hierarchy of several 1D Kernel Density Estimators (KDE)
with a cheap evaluator ([Hyperband], a single multidimensional KDE). Our model
has also incorporated extrapolation based early stopping rule. With our model,
we could achieve a 25% L1 norm for a large-scale BEAM simulation in fully au-
tonomous manner. To the best of our knowledge, our work is the first of its kind
applied to large-scale multi-agent transportation simulations. This work can be
useful for surrogate modeling of scenarios with very large populations. You can find our paper [here] (accepted at [LOD 2022]).

## Usage

1. Clone our repo and initialize submodule HpBandSter (commit: 841db4b) and BEAM (commit: cda7c18)

   ```command
   git clone https://github.com/kiranchhatre/BEAM-Bayes-Opt.git 
   cd BEAM-Bayes-Opt
   git submodule init
   git submodule update
   ```

2. Install requirements 
    
    ```command
    conda env create --BEAMBayesOpt envname --file=environment.yml
    conda activate BEAMBayesOpt
    ```

3. BEAM setup

    System requirements:

        1. Java Runtime Environment or Java Development Kit 1.8
        2. VIA vizualization app: https://simunto.com/via/
        3. Git-LFS: https://git-lfs.github.com/
        4. Gradle: https://gradle.org/install/
    
    Once done set up the Git-LFS configuration and install and test BEAM as follows:


    ```command
    # Git-LFS configuration
    git lfs install
    git lfs env
    git lfs pull
    
    gradle classes # install BEAM

    ./gradlew :run -PappArgs="['--config', 'test/input/beamville/beam.conf']" # run BEAM on toy scenario
    ```
4. HpBandSter setup

    ```
    cd BOHB/
    python setup.py develop --user
    ```
        
5. Run BEAM calibration experiment

    * Change relevant config paths and BEAM scenario you'd like to optimize
    * Change scenario config file parameters as needed in beam/test/input/sf-light/sf-light-0.5k.conf
    * run `python Bayesian-worker-optimizer/BeamOptimizer.py`



Parallel runs are executed through Pyro from the HpBandSter implementation as follows:

```python
import core.nameserver as hpns
NS = hpns.NameServer(run_id='BEAM', host='127.0.0.1', port=None)
NS.start()

    # Code

NS.shutdown()
```

More information for BEAM can be found in [BEAM docs](https://beam.readthedocs.io/en/latest/index.html) and for HpBandSter in a [blogpost](https://www.automl.org/blog_bohb/).


## Citation
If you find our work useful for your research, please consider citing the paper:
```
@misc{https://doi.org/10.48550/arxiv.2207.05041,
  doi = {10.48550/ARXIV.2207.05041},
  url = {https://arxiv.org/abs/2207.05041},
  author = {Chhatre, Kiran and Feygin, Sidney and Sheppard, Colin and Waraich, Rashid},
  keywords = {Machine Learning (cs.LG), Multiagent Systems (cs.MA), FOS: Computer and information sciences, FOS: Computer and information sciences},
  title = {Parallel Bayesian Optimization of Agent-based Transportation Simulation},
  publisher = {arXiv},
  year = {2022},
  copyright = {Creative Commons Attribution Non Commercial Share Alike 4.0 International}
}
```

## Acknowledgement

The authors would like to thank the BEAM team for technical support. The research is supported by Berkeley Lab fellowship 
and the German National Scholarship provided by the Hans Hermann Voss Foundation.

---------------------------------------

<sup>*</sup> Work was done as Berkeley Lab affiliate, now at [KTH, Sweden]

[Kiran Chhatre]: https://www.kth.se/profile/chhatre
[Sidney Feygin]: https://scholar.google.com/citations?user=9yN4n6kAAAAJ&hl=en
[Colin Sheppard]: https://www.ocf.berkeley.edu/~colinsheppard/
[Rashid Waraich]: https://eta.lbl.gov/people/rashid-waraich
[here]: https://arxiv.org/pdf/2207.05041.pdf
[MATSim]: https://github.com/matsim-org/matsim-libs
[BEAM]: https://github.com/LBNL-UCB-STI/beam
[HpBandSter]: https://github.com/automl/HpBandSter
[Hyperband]: https://github.com/zygmuntz/hyperband
[Energy Technologies Area, Berkeley Lab]: https://transportation.lbl.gov/beam
[Marain.ai]: https://www.marain.com/
[KTH, Sweden]: https://www.kth.se/
[BrightDrop]: https://www.gm.com/brightdrop
[LOD 2022]: https://lod2022.icas.cc/

