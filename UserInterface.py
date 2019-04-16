from Commands import getCommands


class UI:

    def command(self, inStr):
        command = ' '.join(inStr.split(' '))

        command = command.split()

        commandList = getCommands()

        for a in commandList:
            if a.opcode == command[0].lower():
                if len(command)-1 != a.arguments:
                    return a.opcode + " requires " + str(a.arguments) + " arguments"

                if a.arguments == 1:
                    return a.function(command[1])
                elif a.arguments == 2:
                    return a.function(command[1], command[2])
                elif a.arguments == 3:
                    return a.function(command[1], command[2], command[3])
                elif a.arguments == 4:
                    return a.function(command[1], command[2], command[3], command[4])
                elif a.arguments == 5:
                    return a.function(command[1], command[2], command[3], command[4], command[5])
                elif a.arguments == 6:
                    return a.function(command[1], command[2], command[3], command[4], command[5], command[6])
                elif a.arguments == 7:
                    return a.function(command[1], command[2], command[3], command[4], command[5], command[6], command[7])
                elif a.arguments == 8:
                    return a.function(command[1], command[2], command[3], command[4], command[5], command[6],
                                      command[7], command[8])

        return command[0] + " is an unsupported command"

