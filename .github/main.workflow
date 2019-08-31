workflow "CI" {
    on = "pull_request"
    resolves = "HYPOTHESISTEST" 
}

action "HYPOTHESISTEST" {
    uses = "docker://debian:latest"
}

