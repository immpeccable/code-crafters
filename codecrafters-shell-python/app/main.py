import sys
import os
import subprocess
import shlex


def execute_external_program(absolute_path, args):
    result = subprocess.run(
        [f"{absolute_path}", *args],
        capture_output=True,
        text=True
    )

    sys.stdout.write(result.stdout.rstrip())


def check_if_executable(keyword):
    return locate_executable(keyword) is not None


def locate_executable(keyword):
    paths = os.environ['PATH'].split(":")
    for path in paths:
        try:
            all_elements_under_path = os.listdir(path)
        except Exception as e:
            continue
        for element in all_elements_under_path:
            full_path = os.path.join(path, element)
            if element == keyword:
                return full_path
    return None


def handle_type_command(command):
    built_ins = ['echo', 'exit', 'type', 'pwd', 'cd']
    if command in built_ins:
        return sys.stdout.write(f"{command} is a shell builtin")

    full_path = locate_executable(command)
    if full_path:
        return sys.stdout.write(f"{command} is {full_path}")

    sys.stdout.write(f"{command}: not found")


def handle_echo_command(text):
    args = transform_args_with_single_quote(text)
    sys.stdout.write(f"{args}")


def handle_exit():
    exit(0)


def handle_fallback(inp):
    all = shlex.split(inp)
    command = all[0]
    full_path = locate_executable(command)
    if full_path is not None:
        return execute_external_program(full_path, all[1:])

    sys.stdout.write(f"{command}: command not found")


def handle_pwd_command():
    sys.stdout.write(os.getcwd())


def handle_cd_command(path):
    try:
        if path == '~':
            os.chdir(os.path.expanduser("~"))
        else:
            os.chdir(path)
    except Exception as e:
        sys.stdout.write(f"cd: {path}: No such file or directory\n")


def transform_args_with_single_quote(args):
    args = shlex.split(args)
    for index, arg in enumerate(args):
        if (arg[0] == "'" and arg[-1] == "'") or (arg[0] == '"' and arg[-1] == '"'):
            args[index] = arg[1:-1]
    return " ".join(args)


def repl():
    sys.stdout.write("$ ")
    inp = input()
    command_end = inp.find(" ")
    command = inp if command_end == -1 else inp[:command_end]
    args = None if command_end == -1 else inp[command_end+1:]

    match command:
        case 'type':
            handle_type_command(args)
        case 'echo':
            handle_echo_command(args)
        case 'exit':
            handle_exit()
        case 'pwd':
            handle_pwd_command()
        case 'cd':
            handle_cd_command(args)
        case _:
            handle_fallback(inp)
    if command != 'cd':
        sys.stdout.write('\n')


def main():
    while True:
        repl()


if __name__ == "__main__":
    main()
