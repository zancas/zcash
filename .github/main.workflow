workflow "buildimage" {
    on = "pull_request"
    resolves = "build"
}

action "build" {
    uses = "./.github/build"
}

