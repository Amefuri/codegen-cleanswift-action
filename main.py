from enum import Enum
import sys
import os

interactorProtocolMarker = '// MARK: - EndBusinessLogicType'
interactorMarker = '// MARK: - EndBusinessLogic'
presenterProtocolMarker = '// MARK: - EndPresentationLogicType'
presenterMarker = '// MARK: - EndPresentationLogic'
viewControllerProtocolMarker = '// MARK: - EndDisplayLogicType'
viewControllerMarker = '// MARK: - EndDisplayLogic'

lowerFirst = lambda s: s[:1].lower() + s[1:] if s else ''
upperFirst = lambda s: s[:1].upper() + s[1:] if s else ''

class ComponentType(Enum):
    INTERACTOR = 1
    PRESENTER = 2
    VIEWCONTROLLER = 3
    MODEL = 4

def generateModel(sceneName: str, actionName: str):
    fileName = getFileName(ComponentType.MODEL, sceneName)
    inputfile = open(fileName, 'r').readlines()
    write_file = open(fileName,'w')
    for index, line in enumerate(inputfile):
        if line.rstrip("\n") == '}':
            new_line = f'\n{"".ljust(indentSize)}enum {upperFirst(actionName)} {{\n\n{"".ljust(indentSize)}{"".ljust(indentSize)}struct Request {{\n\n{"".ljust(indentSize)}{"".ljust(indentSize)}}}\n\n{"".ljust(indentSize)}{"".ljust(indentSize)}struct Response {{\n\n{"".ljust(indentSize)}{"".ljust(indentSize)}}}\n\n{"".ljust(indentSize)}{"".ljust(indentSize)}struct ViewModel {{\n\n{"".ljust(indentSize)}{"".ljust(indentSize)}}}\n{"".ljust(indentSize)}}}'
            write_file.write(new_line + "\n")
        write_file.write(line)
    write_file.close()


def generateAction(componentType: ComponentType, sceneName: str, actionName: str):
    fileName = getFileName(componentType, sceneName)
    inputfile = open(fileName, 'r').readlines()
    write_file = open(fileName,'w')
    for index, line in enumerate(inputfile):
        if index < len(inputfile) - 1 :
            if getProtocolMarkerName(componentType) in inputfile[index+1]:
                if line.strip() != '':
                    write_file.write(line)
                new_line = f'{"".ljust(indentSize)}{getFunctionName(componentType, sceneName, actionName)}'
                write_file.write(new_line + "\n\n")
                continue
            elif getMarkerName(componentType) in inputfile[index+1]:
                if line.strip() != '':
                    write_file.write(line)
                new_line = f'\n{"".ljust(indentSize)}{getFunctionName(componentType, sceneName, actionName)} {{\n\n{"".ljust(indentSize)}}}'
                write_file.write(new_line + "\n")
        write_file.write(line)
    write_file.close()

def getFileName(componentType: ComponentType, sceneName: str):
    if componentType == ComponentType.INTERACTOR:
        return f'{upperFirst(sceneName)}Interactor.swift' #os.path.join(sys.path[0], f'{upperFirst(sceneName)}Interactor.swift') 
    elif componentType == ComponentType.PRESENTER:
        return f'{upperFirst(sceneName)}Presenter.swift' #os.path.join(sys.path[0], f'{upperFirst(sceneName)}Presenter.swift') 
    elif componentType == ComponentType.VIEWCONTROLLER:
        return f'{upperFirst(sceneName)}ViewController.swift' #os.path.join(sys.path[0], f'{upperFirst(sceneName)}ViewController.swift') 
    elif componentType == ComponentType.MODEL:
        return f'{upperFirst(sceneName)}Models.swift' #os.path.join(sys.path[0], f'{upperFirst(sceneName)}Models.swift') 
    else:
        return ''

def getProtocolMarkerName(componentType: ComponentType):
    if componentType == ComponentType.INTERACTOR:
        return interactorProtocolMarker
    elif componentType == ComponentType.PRESENTER:
        return presenterProtocolMarker
    elif componentType == ComponentType.VIEWCONTROLLER:
        return viewControllerProtocolMarker
    else:
        return ''

def getMarkerName(componentType: ComponentType):
    if componentType == ComponentType.INTERACTOR:
        return interactorMarker
    elif componentType == ComponentType.PRESENTER:
        return presenterMarker
    elif componentType == ComponentType.VIEWCONTROLLER:
        return viewControllerMarker
    else:
        return ''

def getFunctionName(componentType: ComponentType, sceneName: str, actionName: str):
    if componentType == ComponentType.INTERACTOR:
        return f'func {lowerFirst(actionName)}(request: {sceneName}.{upperFirst(actionName)}.Request)'
    elif componentType == ComponentType.PRESENTER:
        return f'func present{upperFirst(actionName)}(response: {sceneName}.{upperFirst(actionName)}.Response)'
    elif componentType == ComponentType.VIEWCONTROLLER:
        return f'func display{upperFirst(actionName)}(viewModel: {sceneName}.{upperFirst(actionName)}.ViewModel)'
    else:
        return ''

print('Binary version: 1.0.1')
indentSize = int(input("Enter indent(2 or 4): "))
sceneName = input("Enter sceneName(ex. ChatRoomList): ")
actionName = input("Enter actionName(ex. FetchList): ")

generateAction(ComponentType.INTERACTOR, sceneName, actionName)
generateAction(ComponentType.PRESENTER, sceneName, actionName)
generateAction(ComponentType.VIEWCONTROLLER, sceneName, actionName)
generateModel(sceneName, actionName)

print('DONE')