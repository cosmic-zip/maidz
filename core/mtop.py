import os
import sys
import platform
from core.core import puts


def get_ram_usage():
    with open("/proc/meminfo", "r") as f:
        lines = f.readlines()
    mem_total = int(lines[0].split()[1])
    mem_free = int(lines[1].split()[1])
    mem_available = int(lines[2].split()[1])
    return mem_total, mem_free, mem_available


def get_desktop_environment():
    desktop_session = os.environ.get("DESKTOP_SESSION")
    if desktop_session:
        if desktop_session == "ubuntu":
            return "GNOME"
        return desktop_session
    elif os.environ.get("GNOME_DESKTOP_SESSION_ID"):
        return "GNOME"
    elif os.environ.get("KDE_FULL_SESSION"):
        return "KDE"
    elif os.environ.get("XDG_CURRENT_DESKTOP"):
        return os.environ.get("XDG_CURRENT_DESKTOP")
    else:
        return "Unknown"


def mtop():

    with open("/proc/loadavg", "r") as f:
        load_avg = f.readline().strip().split()[:3]
    cpu_load = tuple(float(x) for x in load_avg)

    mem_total, mem_free, mem_available = get_ram_usage()
    os_name = platform.system()
    kernel_version = platform.release()
    shell = os.environ.get("SHELL")
    desktop_environment = get_desktop_environment()

    var = f"""
        [?25l[0m [38;2;0;0;0m                      [38;2;52;62;50m▅[38;2;31;39;27m▁  [0m [38;2;152;158;151m▂[38;2;226;227;227m▂[38;2;245;245;245m▂[38;2;240;241;240m▂[38;2;226;229;229m▂[38;2;204;213;207m▁[0m [38;2;0;0;0m               [0m
        [38;2;0;0;0m                     [7m[38;2;39;52;31m▊[0m[38;2;60;63;60;48;2;75;74;75m▍[38;2;47;49;45;48;2;68;69;68m┊[0m[38;2;205;205;205m▄[38;2;190;191;189m▆[38;2;42;42;41;48;2;211;214;210m▂[38;2;32;32;32;48;2;233;233;234m▃[38;2;57;57;57;48;2;243;243;243m▄[38;2;24;24;23;48;2;226;226;226m▃[38;2;56;56;56;48;2;248;248;248m▃[38;2;79;79;79;48;2;250;251;251m▂[38;2;129;129;129;48;2;243;243;242m▁[38;2;247;248;247;48;2;152;162;150m▇[0m[38;2;223;225;222m▆[38;2;196;199;194m▄[38;2;130;139;129m▁            [0m
        [38;2;0;0;0m                     [7m[38;2;37;43;33m▍[0m[38;2;121;123;124;48;2;74;73;73m▝[38;2;92;92;93;48;2;162;162;162m▆[38;2;97;97;98;48;2;146;146;146m▇[38;2;55;55;56;48;2;99;99;99m▆[38;2;41;41;41;48;2;36;36;36m▏[38;2;36;36;36;48;2;31;31;31m▂[38;2;34;34;34;48;2;29;29;29m▂[38;2;32;32;32;48;2;28;28;28m▃[38;2;31;31;31m▃[38;2;30;30;30m▃[48;2;20;20;20m▆[38;2;37;37;37;48;2;197;197;197m▇[38;2;43;43;43m▄[38;2;120;120;120;48;2;234;234;234m▃[38;2;251;250;249;48;2;239;241;239m┈[0m[38;2;193;197;194m▅[0m [38;2;42;49;42m [38;2;41;55;31m▁[38;2;45;54;42m▂[38;2;48;59;44m▃[0m [38;2;3;5;2m     [0m
        [38;2;0;0;0m                    [38;2;30;37;24m▗[7m[38;2;47;47;47m▘[0m[38;2;48;48;48;48;2;79;79;78m▆[38;2;68;68;69;48;2;53;53;53m▗[38;2;110;110;112;48;2;81;81;82m▄[38;2;78;78;79;48;2;54;54;55m▃[38;2;122;122;122;48;2;52;52;52m▂[38;2;72;72;72;48;2;48;48;48m▂[38;2;82;82;82;48;2;49;49;49m▁[38;2;55;55;55;48;2;41;41;41m▃[38;2;51;51;51;48;2;39;39;39m▄[38;2;48;48;48;48;2;37;37;37m▄[38;2;47;47;47m▄[38;2;49;49;49;48;2;39;39;39m▃[38;2;46;46;46m▅[48;2;117;116;117m▉[38;2;102;102;102;48;2;230;230;230m▂[38;2;243;243;243;48;2;247;247;248m▊[38;2;43;49;42;48;2;193;193;193m▝[38;2;141;141;140;48;2;53;56;53m▂[38;2;100;101;100;48;2;57;57;57m▄[38;2;56;59;61;48;2;69;69;68m▗[0m[38;2;45;53;42m▍      [0m
        [38;2;0;0;0m                   [0m [38;2;20;24;16;48;2;35;37;34m▏[38;2;39;39;39;48;2;41;41;41m▄[38;2;45;45;45;48;2;42;42;42m▝[38;2;51;50;50;48;2;48;47;47m┊[38;2;111;111;107;48;2;50;49;48m╻[38;2;69;68;68;48;2;50;50;50m▝[38;2;52;52;52;48;2;91;91;91m▆[38;2;45;45;46;48;2;76;76;78m▅[38;2;59;59;59;48;2;98;98;100m▄[38;2;54;54;54;48;2;112;112;114m▄[38;2;85;85;87;48;2;63;63;64m▝[38;2;104;104;104;48;2;66;66;66m▘[38;2;147;147;147;48;2;83;83;83m━[38;2;130;130;130;48;2;63;63;63m▗[38;2;146;146;146;48;2;72;72;72m▖[38;2;95;95;95;48;2;61;61;61m▅[38;2;94;94;94;48;2;160;160;160m▉[38;2;201;201;201;48;2;238;238;238m▁[38;2;244;244;244;48;2;152;152;152m▋[38;2;191;191;191;48;2;130;130;130m▆[38;2;188;188;188;48;2;104;104;104m╸[0m[7m[38;2;45;50;43m▗[0m[38;2;7;9;5m       [0m
        [38;2;0;0;0m                  [38;2;63;72;53m┗[7m[38;2;37;40;34m▖[0m[38;2;32;32;32;48;2;44;44;44m▇[38;2;36;36;36;48;2;38;38;38m▅[48;2;39;39;39m┈[38;2;226;212;199;48;2;60;57;54m▗[38;2;217;206;196;48;2;47;44;41m▌[38;2;37;37;37;48;2;41;40;41m▄[38;2;26;26;26;48;2;39;39;39m▗[38;2;25;25;25;48;2;34;34;34m▏[38;2;43;43;43;48;2;42;42;42m┊[38;2;173;165;159;48;2;39;39;38m▗[38;2;102;98;93;48;2;45;45;44m▏[38;2;43;43;42;48;2;50;50;50m▆[38;2;44;44;44;48;2;52;52;52m▆[38;2;50;50;50;48;2;66;66;66m▇[38;2;54;54;54;48;2;76;76;76m▆[38;2;51;51;51;48;2;66;66;66m▅[38;2;62;62;62;48;2;50;50;50m▘[38;2;70;70;70;48;2;205;205;205m▊[38;2;139;139;139;48;2;195;195;195m▖[38;2;59;58;59;48;2;162;162;162m▁[38;2;61;64;60;48;2;22;26;20m▊[0m [38;2;16;21;11m       [0m
        [38;2;0;0;0m                  [38;2;30;39;23m┏[38;2;36;43;30;48;2;21;21;21m▘[38;2;38;38;38;48;2;33;33;34m┛[38;2;38;37;37;48;2;97;94;89m▉[38;2;126;123;117;48;2;57;54;51m▎[38;2;100;92;85;48;2;225;208;193m▏[38;2;71;65;63;48;2;216;200;188m▝[38;2;31;32;31;48;2;34;34;33m┊[38;2;16;16;17;48;2;29;28;28m╱[38;2;32;34;37;48;2;43;41;40m╴[38;2;176;169;164;48;2;76;72;69m▖[38;2;79;73;68;48;2;209;194;180m▘[38;2;214;199;186;48;2;49;47;45m▎[38;2;36;36;36;48;2;39;40;38m▇[48;2;39;39;39m▄[38;2;44;44;44m▝[38;2;41;41;41;48;2;45;45;45m▄[38;2;42;42;42m▃[38;2;43;43;43;48;2;46;46;46m▃[38;2;44;44;44;48;2;39;39;39m▖[38;2;133;133;133;48;2;76;75;76m╹[38;2;35;38;35;48;2;25;31;22m▉[0m [38;2;23;30;20m        [0m
        [38;2;0;0;0m                  [7m[38;2;34;40;27m▖[0m[38;2;34;34;36;48;2;24;26;24m╶[38;2;40;40;41;48;2;33;32;32m╷[38;2;197;188;179;48;2;73;63;62m▅[38;2;201;196;194;48;2;77;76;94m▋[38;2;36;34;60;48;2;186;172;159m▆[38;2;110;101;114;48;2;245;226;211m▖[38;2;33;30;27;48;2;221;205;193m▝[38;2;223;206;195;48;2;63;62;59m▄[38;2;241;223;210;48;2;131;122;115m▇[38;2;138;128;120;48;2;234;217;204m╹[38;2;108;94;84;48;2;248;229;213m▁[38;2;212;198;186;48;2;78;72;67m▍[38;2;177;167;159;48;2;58;54;49m▊[38;2;32;31;31;48;2;33;34;33m▁[38;2;34;34;35;48;2;36;36;35m▄[38;2;35;35;35;48;2;38;38;38m▃[38;2;37;37;37;48;2;39;39;39m▄[38;2;38;38;38;48;2;41;41;41m▄[38;2;39;38;39;48;2;22;22;21m▊[38;2;39;41;38;48;2;23;26;22m▉[0m[38;2;53;64;51m▘         [0m    {f"⬥ CPU: {cpu_load[1]*100}%"}
        [38;2;0;0;0m                   [7m[38;2;33;36;29m▏[0m[38;2;41;38;38;48;2;155;143;136m▉[38;2;254;233;221;48;2;242;224;212m╴[38;2;145;143;157;48;2;250;234;223m▝[38;2;237;221;212;48;2;49;53;90m▅[38;2;245;229;217;48;2;171;163;167m▇[38;2;251;234;219;48;2;252;234;218m┯[38;2;252;234;218;48;2;252;233;221m▋[38;2;252;233;219;48;2;251;233;222m▊[38;2;231;220;213;48;2;99;97;107m▉[38;2;53;59;97;48;2;34;35;66m▁[38;2;96;99;131;48;2;25;25;54m▁[38;2;202;197;196;48;2;65;54;50m▆[38;2;77;70;69;48;2;32;31;31m▏[38;2;33;33;33;48;2;33;32;32m╴[38;2;18;18;18;48;2;30;30;30m╻[38;2;34;34;34;48;2;37;37;37m╴[38;2;49;49;49;48;2;35;35;35m▍[38;2;12;13;13;48;2;30;29;30m╻[0m[38;2;61;65;59m▌          [0m    {f"⬥ Total RAM: {int(mem_total/1024)} MB"}
        [38;2;0;0;0m                  [7m[38;2;37;45;30m▊[0m[38;2;64;63;60;48;2;55;56;54m╴[38;2;77;68;66;48;2;50;49;49m▝[38;2;104;89;86;48;2;238;218;207m▖[38;2;252;231;218;48;2;252;232;218m▁[38;2;252;233;219;48;2;251;235;218m▆[48;2;251;235;217m▆[48;2;252;233;218m┷[38;2;253;234;217;48;2;252;234;218m╺[38;2;252;235;218;48;2;252;233;218m▆[38;2;252;233;219;48;2;245;231;222m▇[38;2;242;225;215;48;2;92;92;116m▇[38;2;244;228;217;48;2;117;117;136m▇[38;2;138;131;122;48;2;238;222;210m▝[38;2;140;133;125;48;2;60;56;54m┛[38;2;56;52;53;48;2;39;37;38m╻[38;2;74;75;75;48;2;32;32;32m▂[38;2;47;47;47;48;2;31;31;31m▍[38;2;46;43;44;48;2;35;35;35m▂[38;2;28;26;26;48;2;38;40;37m╸[0m[38;2;47;56;43m▘          [0m    {f"⬥ Free RAM: {int(mem_free/1024)} MB"}
        [38;2;0;0;0m                  [7m[38;2;46;49;41m▘[0m[38;2;40;41;40;48;2;44;44;44m▂[38;2;135;135;135;48;2;59;59;60m┏[38;2;119;122;123;48;2;77;75;73m╷[38;2;60;52;47;48;2;223;204;194m▖[38;2;251;232;218;48;2;251;231;218m┊[38;2;249;229;216;48;2;251;232;218m╺[38;2;244;225;211;48;2;252;233;218m╾[38;2;251;233;219m┳[38;2;252;233;219;48;2;252;235;219m▅[38;2;253;233;218;48;2;252;232;218m╴[38;2;250;212;206;48;2;252;231;219m▂[38;2;247;196;196;48;2;251;227;216m▃[38;2;108;88;85;48;2;221;180;181m▝[38;2;149;126;127;48;2;67;53;54m╍[38;2;104;97;95;48;2;43;41;41m╸[38;2;124;124;124;48;2;77;77;77m┛[38;2;22;23;21;48;2;33;33;33m▆[0m[7m[38;2;34;41;27m▆[0m [38;2;0;0;0m           [0m    {f"⬥ Available RAM: {int(mem_available/1024)} MB"}
        [38;2;0;0;0m                 [7m[38;2;35;45;28m▊[0m[38;2;39;41;39;48;2;38;39;37m┈[38;2;37;37;36;48;2;67;65;66m▉[38;2;62;64;63;48;2;175;175;175m▗[38;2;116;115;115;48;2;36;36;36m▘[38;2;32;35;33;48;2;35;34;34m╴[38;2;47;35;36;48;2;173;157;157m╾[38;2;173;153;153;48;2;239;219;208m▖[38;2;188;169;170;48;2;251;229;218m▂[38;2;213;193;192;48;2;236;215;207m╻[38;2;195;154;154;48;2;234;214;209m╶[38;2;131;89;101;48;2;226;202;212m─[38;2;128;94;102;48;2;223;195;213m━[38;2;63;55;60;48;2;197;152;156m▆[38;2;22;22;24;48;2;36;30;30m╴[38;2;54;53;54;48;2;22;23;23m▖[38;2;48;48;48;48;2;57;56;57m▚[38;2;46;46;46;48;2;26;26;26m▋[38;2;21;21;21;48;2;36;38;34m┊[0m [38;2;43;55;26m            [0m    {f"⬥ OS Name: {os_name}"}
        [38;2;0;0;0m                 [7m[38;2;42;47;36m▍[0m[38;2;29;29;32;48;2;33;33;34m╴[38;2;53;54;55;48;2;33;31;33m▎[38;2;127;113;177;48;2;49;48;50m▂[38;2;132;125;176;48;2;64;62;62m▃[38;2;199;194;196;48;2;110;102;104m▗[38;2;252;253;253;48;2;250;250;251m┊[38;2;253;252;253;48;2;253;251;252m▇[48;2;253;253;253m [38;2;252;253;253;48;2;252;252;253m╺[38;2;250;249;250;48;2;252;252;251m▁[38;2;212;215;249;48;2;242;243;252m▝[38;2;204;213;252;48;2;209;213;251m┊[38;2;209;202;227;48;2;45;39;43m▎[38;2;20;22;21;48;2;33;33;33m▍[38;2;66;66;66;48;2;31;31;31m▎[38;2;59;59;59;48;2;43;43;43m▎[38;2;23;23;23;48;2;32;32;32m╱[38;2;32;32;32;48;2;45;47;41m▉[0m[38;2;45;54;37m▎            [0m    {f"⬥ Kernel Version: {kernel_version}"}
        [38;2;0;0;0m                 [7m[38;2;82;86;79m▎[0m[38;2;94;92;149;48;2;45;43;48m▂[38;2;58;49;70;48;2;126;120;197m▘[38;2;136;134;183;48;2;133;124;203m▅[38;2;171;169;172;48;2;97;90;130m▄[38;2;138;138;137;48;2;204;203;205m▃[38;2;141;141;141;48;2;241;241;241m╼[38;2;247;247;247;48;2;234;234;235m┈[38;2;236;236;236;48;2;247;247;247m▖[38;2;242;242;242;48;2;250;250;250m─[38;2;233;234;234;48;2;247;247;247m▗[38;2;232;232;233;48;2;248;248;248m▂[38;2;80;78;91;48;2;222;223;234m╺[38;2;152;145;160;48;2;55;49;50m▎[38;2;34;34;34;48;2;23;23;23m▏[38;2;56;56;56;48;2;36;36;36m┍[38;2;18;18;18;48;2;26;26;26m▗[38;2;52;52;52;48;2;32;32;32m┓[38;2;33;33;33;48;2;35;32;34m▊[0m[7m[38;2;35;38;33m▝[0m [38;2;20;24;14m           [0m    {f"⬥ Shell: {shell}"}
        [38;2;0;0;0m               [0m [38;2;77;72;62m▂[7m[38;2;119;117;164m▘[0m[38;2;106;102;117;48;2;126;124;190m▗[38;2;215;214;213;48;2;100;94;123m▂[38;2;241;240;242;48;2;113;110;116m▄[38;2;235;235;236;48;2;109;109;110m▇[38;2;226;226;228;48;2;239;239;240m┓[38;2;75;75;75;48;2;238;238;238m▁[38;2;78;78;78;48;2;250;250;250m▃[38;2;62;62;62;48;2;247;247;247m▄[38;2;65;65;65;48;2;251;251;251m▅[38;2;69;68;69;48;2;242;242;242m▄[38;2;51;50;56;48;2;226;226;227m▂[38;2;139;140;151;48;2;236;237;244m▁[38;2;217;218;225;48;2;69;67;71m▋[38;2;18;18;19;48;2;34;34;34m▉[38;2;62;62;63;48;2;31;31;31m▏[38;2;25;25;25;48;2;28;28;28m▏[38;2;73;73;73;48;2;34;34;34m╻[38;2;46;47;46;48;2;34;35;34m┒[38;2;32;32;31;48;2;25;28;27m▉[0m[7m[38;2;35;42;27m╻[0m[38;2;45;54;37m▃          [0m    {f"⬥ Desktop Environment: {desktop_environment}"}
        [38;2;0;0;0m            [0m [38;2;173;171;166m▃[38;2;140;134;136m▅[38;2;214;214;214;48;2;95;91;86m▄[38;2;245;245;244;48;2;131;119;124m▅[38;2;239;239;242;48;2;132;126;157m▆[38;2;246;246;246;48;2;168;169;167m▇[38;2;135;135;135;48;2;243;243;244m▂[38;2;69;68;72;48;2;223;222;228m▃[38;2;63;63;65;48;2;201;200;207m▅[38;2;57;57;57;48;2;173;173;174m▇[38;2;65;65;65;48;2;45;45;45m╸[38;2;43;43;43;48;2;46;46;46m┈[38;2;44;44;44m╴[48;2;45;45;45m╴[38;2;45;44;46;48;2;50;47;47m▄[38;2;49;42;48;48;2;44;38;45m╸[38;2;66;62;70;48;2;166;161;169m▉[38;2;188;182;188;48;2;79;73;78m▉[38;2;30;29;32;48;2;23;21;24m┃[38;2;62;63;62;48;2;30;30;30m▏[38;2;16;16;16;48;2;28;28;28m╻[38;2;65;65;65;48;2;39;39;39m▗[38;2;25;25;25;48;2;32;32;31m╴[38;2;29;29;29;48;2;34;34;34m┒[0m[38;2;37;41;32m▋[0m  [38;2;0;0;0m         [0m     
        [38;2;0;0;0m          [0m [38;2;215;213;210m▃[38;2;235;233;234;48;2;133;131;121m▆[38;2;249;250;250;48;2;169;167;168m▆[38;2;253;253;253;48;2;249;249;249m┈[38;2;234;233;239;48;2;250;250;251m▗[38;2;229;228;234;48;2;245;244;246m▝[38;2;237;236;241;48;2;232;232;236m┊[38;2;237;236;238;48;2;83;83;85m▘[38;2;42;42;42;48;2;43;43;43m╴[38;2;43;43;43;48;2;50;50;50m▇[38;2;44;44;44;48;2;42;42;42m▄▆[48;2;45;45;45m▘[38;2;45;46;46m▃[38;2;46;46;46m▆[48;2;45;45;44m▍[38;2;44;44;45;48;2;40;39;44m▋[38;2;39;39;44;48;2;40;38;45m▄[38;2;55;46;54;48;2;116;98;105m▊[38;2;206;196;198;48;2;67;50;55m▋[38;2;35;33;34;48;2;24;26;25m▉[38;2;22;22;22;48;2;32;32;32m▏[38;2;23;23;23;48;2;32;33;32m▝[38;2;26;26;26;48;2;31;31;31m┈[38;2;81;81;81;48;2;38;38;38m╲[38;2;33;33;33;48;2;29;29;29m▇[38;2;27;27;27;48;2;33;35;32m┑[0m[38;2;38;44;33m▖          [0m    ☺  ☻  ♥  ♦  ♣  ♠  •  ◘
        [38;2;0;0;0m         [0m [7m[38;2;222;219;220m▘[0m[38;2;234;235;237;48;2;250;249;250m▘[38;2;253;253;253;48;2;253;252;252m┊[48;2;252;252;251m▊[38;2;221;220;225;48;2;245;244;246m┏[38;2;250;249;253;48;2;247;246;249m┊[38;2;244;244;242;48;2;252;252;252m▘[38;2;223;223;229;48;2;76;75;81m▋[38;2;43;43;45;48;2;41;41;41m▎[38;2;42;42;42;48;2;43;43;43m▋[48;2;44;44;44m [48;2;45;45;45m [48;2;46;46;46m    [38;2;46;46;46;48;2;45;45;45m▋[38;2;42;42;45;48;2;44;44;45m▝[38;2;41;42;45;48;2;39;40;45m▖[38;2;60;51;58;48;2;120;98;105m▉[38;2;128;108;113;48;2;51;45;46m▏[38;2;36;36;36;48;2;35;35;35m╌[48;2;39;39;40m▉[0m[7m[38;2;48;53;43m▗[38;2;32;34;31m▖[0m[38;2;52;51;50;48;2;45;45;45m╷[38;2;61;61;61;48;2;38;38;38m╲[38;2;35;36;33;48;2;34;34;34m╴[38;2;22;24;22;48;2;32;34;29m╶[0m[38;2;37;46;28m▖         [0m    ○  ◙  ♂  ♀  ♪  ♫  ☼  ►
        [38;2;0;0;0m         [7m[38;2;218;213;215m▋[0m[38;2;246;246;246;48;2;233;234;234m▇[48;2;253;253;253m  [38;2;221;220;226;48;2;250;250;250m▗[38;2;226;225;232;48;2;223;222;228m╺[38;2;226;225;231;48;2;240;240;243m┐[38;2;221;224;249;48;2;251;251;253m▃[38;2;181;182;196;48;2;59;59;68m▎[38;2;39;38;44;48;2;42;42;42m▃[38;2;64;65;66;48;2;46;46;47m╷[48;2;45;45;45m [38;2;46;46;46;48;2;46;45;46m┈[48;2;46;46;46m     [38;2;45;45;45;48;2;44;44;44m▇[38;2;41;40;46;48;2;44;44;46m▝[38;2;40;40;45;48;2;43;40;46m┊[38;2;97;87;93;48;2;45;36;41m▗[38;2;35;35;35;48;2;39;39;39m┊[38;2;36;37;37;48;2;36;36;37m┈[0m[38;2;36;39;33m▉[0m [7m[38;2;29;33;24m▃[0m[38;2;80;79;78;48;2;37;39;35m╲[38;2;46;46;46;48;2;30;30;30m▏[38;2;35;35;33;48;2;34;35;33m┊[0m [38;2;30;40;18m         [0m    ◄  ↕  ‼  ¶  §  ▬  ↨  ↑
        [38;2;0;0;0m         [7m[38;2;202;198;195m▋[0m[38;2;236;235;234;48;2;252;252;252m▏[38;2;253;253;252;48;2;253;252;253m▁[38;2;254;252;253;48;2;252;252;252m╴[38;2;211;210;218;48;2;227;227;238m╹[38;2;210;214;249;48;2;225;225;240m▃[38;2;196;199;233;48;2;135;138;168m▉[38;2;57;58;70;48;2;190;195;231m▅[38;2;37;39;45;48;2;39;41;49m┈[38;2;36;38;45;48;2;38;38;45m╱[38;2;43;39;46;48;2;66;64;68m▇[38;2;75;61;67;48;2;58;52;54m╴[48;2;46;45;46m [38;2;46;45;45m▂[48;2;46;46;46m [38;2;46;46;46;48;2;46;46;45m┈[48;2;46;46;46m  [48;2;46;46;45m┈[48;2;45;45;45m [38;2;44;43;45;48;2;41;40;45m▋[38;2;44;36;44;48;2;49;43;50m┊[38;2;100;89;95;48;2;129;126;128m▖[38;2;135;135;135;48;2;44;44;45m▖[38;2;37;36;38;48;2;37;38;37m┊[0m[38;2;34;40;27m▌ [38;2;28;35;24m▝[38;2;29;34;24;48;2;36;37;34m▏[38;2;35;36;34;48;2;27;36;18m▉[0m [38;2;30;40;17m         [0m    ↓  →  ←  ∟  ↔  ▲  ▼  *
        [38;2;0;0;0m         [0m [7m[38;2;197;197;191m▖[0m[38;2;252;253;250;48;2;243;243;249m╴[38;2;212;216;249;48;2;242;243;251m▅[38;2;183;188;228;48;2;196;201;238m┓[38;2;128;130;160;48;2;197;202;239m▁[38;2;201;205;242;48;2;67;69;80m▘[38;2;40;39;46;48;2;39;39;46m╴[38;2;41;40;46m▃[38;2;40;40;46;48;2;38;39;44m▂[38;2;37;40;45m╶[38;2;45;40;45;48;2;64;51;55m▉[38;2;74;62;65;48;2;48;46;45m▖[38;2;44;46;45;48;2;46;45;47m▋[38;2;46;45;46;48;2;46;46;45m▏[48;2;46;46;46m   [38;2;45;46;46m┊[38;2;46;46;46;48;2;45;45;45m▋[38;2;44;45;45;48;2;42;43;46m▊[38;2;41;42;47;48;2;40;39;45m▏[38;2;134;126;129;48;2;55;46;54m▝[38;2;149;148;150;48;2;124;124;123m▉[38;2;76;76;76;48;2;37;37;37m▏[0m[38;2;39;45;32m▌ [0m [7m[38;2;37;40;34m▏[38;2;33;37;27m▗[0m[38;2;3;5;2m          [0m
        [38;2;0;0;0m           [7m[38;2;236;232;237m▍[0m[38;2;252;252;252;48;2;217;221;246m▅[38;2;47;47;48;48;2;175;176;192m▗[38;2;45;45;48;48;2;100;100;122m▇[38;2;45;45;45;48;2;40;39;45m▆[48;2;41;41;45m▆[38;2;44;44;45;48;2;42;42;46m▆[38;2;42;42;45;48;2;41;41;46m▄[38;2;40;41;45;48;2;38;40;44m▊[38;2;39;39;46;48;2;44;38;46m▉[38;2;63;51;54;48;2;52;41;46m│[38;2;45;46;44;48;2;46;45;46m▎[38;2;46;46;46;48;2;46;46;45m┈[48;2;46;46;46m    [48;2;45;45;45m▋[38;2;44;44;45;48;2;42;41;46m▊[38;2;40;40;46;48;2;39;40;45m▎[38;2;39;39;45;48;2;55;40;48m▉[38;2;118;106;111;48;2;49;47;42m▘[0m[7m[38;2;33;37;27m▄[0m  [7m[38;2;59;65;54m▘[38;2;41;45;38m▗[0m [38;2;0;0;0m          [0m
        [38;2;0;0;0m           [7m[38;2;229;225;224m▍[0m[38;2;242;242;242;48;2;253;253;252m▁[38;2;216;216;216;48;2;53;53;54m▏[38;2;44;44;44;48;2;46;46;46m▇[48;2;45;45;45m▁[38;2;45;45;45;48;2;46;46;46m▄[38;2;45;45;46;48;2;44;44;45m▝[38;2;44;44;44;48;2;42;42;45m▋[38;2;41;41;45;48;2;39;40;45m▋[38;2;39;39;47;48;2;38;39;45m┊[38;2;49;39;44;48;2;62;53;55m▉[38;2;46;45;43;48;2;47;46;45m╴[48;2;45;45;45m [38;2;45;45;45;48;2;46;46;46m▃▆[38;2;44;44;44;48;2;45;45;45m▅▃[38;2;44;44;45m▂[38;2;43;43;44;48;2;41;40;44m▋[38;2;39;39;45;48;2;39;40;45m▇[48;2;49;39;44m▉[0m[38;2;67;55;45m▎ [38;2;88;97;80m╶[7m[38;2;113;120;107m▃[0m[38;2;47;51;41m▘            [0m
        [38;2;0;0;0m           [7m[38;2;236;233;233m▎[0m[38;2;250;250;250;48;2;229;229;229m▆[38;2;223;223;223;48;2;58;58;58m▆[38;2;217;217;218;48;2;48;48;49m▅[38;2;218;217;221;48;2;52;52;52m▄[38;2;220;220;224;48;2;59;59;60m▃[38;2;210;210;214;48;2;46;46;47m▃[38;2;219;220;225;48;2;56;56;59m▂[38;2;192;194;213;48;2;44;44;50m▂[38;2;156;161;191;48;2;36;37;44m▂[38;2;171;173;212;48;2;44;40;51m▁[38;2;49;47;46;48;2;59;52;55m┊[38;2;46;45;45;48;2;45;45;45m▎[38;2;44;44;44;48;2;43;43;43m▌[38;2;41;41;41m▅[38;2;40;40;40;48;2;42;42;42m▅▅[38;2;39;39;43;48;2;42;42;44m▅[38;2;36;36;41;48;2;39;39;44m▃[38;2;37;38;43;48;2;38;39;44m▃[38;2;36;40;45;48;2;48;46;47m╴[0m [38;2;33;33;23m                [0m
        [38;2;0;0;0m          [7m[38;2;142;141;124m▉[0m[38;2;198;192;186;48;2;245;244;242m▏[38;2;198;203;191;48;2;248;248;248m▁[38;2;183;187;175;48;2;228;228;228m▁[38;2;177;182;171;48;2;223;223;225m▁[38;2;179;184;174;48;2;221;220;225m▁[38;2;181;186;176;48;2;220;220;224m▁[38;2;180;185;176;48;2;220;220;225m▁[38;2;179;185;178;48;2;219;220;226m▁[38;2;177;183;179;48;2;212;214;229m▁[38;2;168;174;182;48;2;190;193;228m▁[38;2;158;168;184;48;2;184;189;231m▁[38;2;81;72;82;48;2;168;167;201m▝[38;2;45;44;45;48;2;55;53;54m┊[38;2;61;66;52;48;2;45;45;44m▁[38;2;62;67;54;48;2;44;44;44m▁[38;2;61;66;52;48;2;44;44;43m▁[38;2;60;66;52;48;2;43;44;43m▁[38;2;60;65;51;48;2;43;43;44m▁[38;2;58;63;51;48;2;40;40;43m▁[38;2;55;61;51;48;2;38;38;43m▁[0m[38;2;54;51;47m▊                 [0m
        [?25h
    """

    puts(var)
