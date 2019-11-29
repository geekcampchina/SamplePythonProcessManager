# Sample Python Process Manager

## Standard signals

注意： `SIGKILL` 信号由于操作系统限制，不能在程序中被捕获。

`man 7 signal`

    Signal      Standard   Action   Comment
    ────────────────────────────────────
    SIGINT       P1990      Term    Interrupt from keyboard
    SIGKILL      P1990      Term    Kill signal
    SIGTERM      P1990      Term    Termination signal
    SIGHUP       P1990      Term    Hangup detected on controlling terminal

## Signal numbering for standard signals

`man 7 signal`

    Signal        x86/ARM     Alpha/   MIPS   PARISC   Notes   most others   SPARC
    ───────────────────────────────────────
    SIGHUP           1           1       1       1
    SIGINT           2           2       2       2
    SIGKILL          9           9       9       9
    SIGTERM         15          15      15      15
