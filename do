## run: Run the app
function task_run() {
    source env/Scripts/activate
    python run.py -p dev
}

## install: Install python requirements into venv
function task_install() {
    python -m venv env
    source env/Scripts/activate
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
}

## test: Run pytest and unittests
function task_test() {
    python -m pytest
    python -W ignore::DeprecationWarning test.py
}

function task_manage_db {
    python manage_db.py
}

function task_usage {
    echo "Usage: $0"
    sed -n 's/^##//p' <"$0" | column -t -s ':' | sed -E $'s/^/\t/'
}

cmd=${1:-}
shift || true
resolved_command=$(echo "task_${cmd}" | sed 's/-/_/g')
if [[ "$(LC_ALL=C type -t "${resolved_command}")" == "function" ]]; then
    pushd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null
    ${resolved_command} "$@"
else
    task_usage
fi