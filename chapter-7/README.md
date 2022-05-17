# What is CI/CD ?

CI/CD is a coding philosophy and set of practices with which you can continuously build, test, and deploy iterative code changes.

This iterative process helps reduce the chance that you develop new code based on buggy or failed previous versions. With this method, you strive to have less human intervention or even no intervention at all, from the development of new code until its deployment.


## Basics of GitHub Actions


Since we are Github for version control system, we can use GitHub Actions right off the bat without having the need to setup another tool. (Might not be the same if you are using different version control system.)

GitHub Actions are just a set instructions declared using `yaml` files.

These files needs to be in a specific folder: `.github/workflows` and this has to be in the root directory (where `.git` folder is present).

There are 5 main concepts in GitHub Actions:

- `Events`: An event is a trigger for workflow.

- `Jobs`: Jobs defines the steps to run when a workflow is triggered. A workflow can contain multiple jobs.

- `Runners`: Defines where to run the code. By default, github will run the code in it's own servers.

- `Steps`: Steps contains actions to run. Each job can contains multiple steps to run.

- `Actions`: Actions contains actual commands to run like installing dependencies, testing code, etc.


### 

Let's create the folder using the command:

```shell
mkdir .github/workflows
```

Now let's create a basic workflow file called `sample.yaml` in that folder and paste the following content.

```yml
name: GitHub Actions Sample Flow
on: [push]
jobs:
  sample-workflow:
    runs-on: ubuntu-latest
    steps:
      - name: Basic Information
        run: |
          echo "🎬 The job was automatically triggered by a ${{ github.event_name }} event."
          echo "💻 This job is now running on a ${{ runner.os }} server hosted by GitHub!"
          echo "🎋 Workflow is running on the branch ${{ github.ref }}"
      - name: Checking out the repository
        uses: actions/checkout@v2
      - name: Information after checking out
        run: |
          echo "💡 The ${{ github.repository }} repository has been cloned to the runner."
          echo "🖥️ The workflow is now ready to test your code on the runner."
      - name: List files in the repository
        run: |
          ls ${{ github.workspace }}
      - run: echo "🍏 This job's status is ${{ job.status }}."
```

Let's understand what's happening here:

- Created a CICD workflow with `name` GitHub Actions Sample Flow

- `on` is called Event which triggers the workflow. Here it is push event. Whenever a push is happened on the repository, workflow will be triggered. There are 30+ ways of triggering the workflow. [Refer to the documentation for more information on events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)

- Workflow contains a single `job` called sample-workflow `running` on ubuntu-latest

- sasic-workflow job contains multiple `steps` (Basic Information, Checking out the repository, Information after checking out, List files in the repository)

- Basic Information step contains the `actions` to do some echoing.

- Checking out the repository step contains the `action` to checkout the repository. Here we are using actions/checkoutv2 which is a open source action. [Check for other available actions here](https://github.com/marketplace?type=actions)

- Information after checking out step contains the `action` to echo some information about repository and runner.

- List files in the repository step contains the `action` to list the contents of the repository.

