# Continuous Integration / Continuous Deployment Excercises

## Introduction

This repository includes a basic example data science project, corresponding unit tests and some pipeline templates that can be used to build a CICD pipeline to lint, test and build the project for deployment.

## Instructions

### Stages

Stages in gitlab allow certain jobs to be grouped together to be run simultaneously. They are defined with the `stage` block and a list of stages can be provided as follows:

```yml
stages:
    - stage1
    - stage2

```

### Jobs

Jobs are where the actions to be taken in the pipeline are defined. Jobs need a job name, `stage`, docker `image` to be run in and `script` of commands to be run in the container at a minimum, such as:

```yml
<job_name>:
    stage: <name 0f stage>
    image: <docker_image_name>
    script:
        - <commands to be run>
```

Jobs with a job name prefixed with a period `.` will not be run when the pipeline is initiated, and are reffered to as hidden jobs. This is useful for creating reusable blocks of code or templates which other jobs can be built out from. When the `extends` keyword is used gitlab combines the configuration in the hidden job with the job extending it. An example of this can be seen below:

```yml
.hidden_job:
    stage: cowsay
    image: bash:latest
    before_script:
        - apt install cowsay

job:
    extends: .hidden_job
    script:
        - cowsay "hello, world"

```

### Import Template Jobs

To aid the devlopment of this pipeline some local and shared templates will be used.

To make use of templates in gitlab pipelines, the templates need to be included using the `include` block which follows the form:

```yml
include:
    - <type>: <location>
```

Template types include - `local`, `remote` & `template`.

## Tasks

1. A `docker-build` job has been included with the `Docker.gitlab-ci.yml` template. Push your newly created branch to the remote to trigger the pipeline. View the pipeline running in the Build > Pipelienes side tab on gitlab.
    1. If the job runs successfully a built container image can be found in the side tab Deploy > Container Registry. There is a ci-cd registry repository and the built image should be tagged with the branch name.
1. The pyproject.toml includes black, flake8 and isort tools to lint the code provided. This task is to create 3 seperate jobs to run these linting tool.
    1. Update the include block to include the `local` template file [templates/.ci-include-linting.yml](./templates/.ci-include-linting.yml). This template includes configuration needeed to install the linting tools.
    1. Define a linting stage for the linting jobs to run in.
    1. Define 3 seperate jobs for each of the linting tools.
    1. In each job extend the hidden job defined in the linting template
    1. Add in the necessary commands to run each of the tools.
        1. isort: `isort src --check-only`
        1. black: `black --check src`
        1. flake8: `flake8 src`
    1. The pipeline is likely to fail due to incorrectly formatted code. Adding an `allow_failure` attribute to the [template file](./templates/.ci-include-linting.yml) and setting it to `true` will allow the rest of the pipeline to continue while still warning of the relevant errors.
1. This task is to create a `testing` stage and subsequent job to run unit tests on the code provided. Create a job with the following spec:
    1. image: `python:3.11.5`
    1. script: `poetry run pytest`
    1. A before script has been provided to configure the container as a [yaml anchor](https://docs.gitlab.com/ee/ci/yaml/yaml_optimization.html#yaml-anchors-for-scripts) and can be inluded in the `before_script` keyword by using `*pytest_before_script`.
1. This task is to consume the image built earlier and run an integration test with some example data in the image.
    1. The image can be found in the following registry address `registry.gitlab.com/facultyai/fellowship/mle-fellowship-teaching-resources/ci-cd:$CI_COMMIT_REF_SLUG` where `$CI_COMMIT_REF_SLUG` is a built in gitlab variable referencing the branch name.
    2. Run the following command to run the test `poetry run python3 -m src.main`
