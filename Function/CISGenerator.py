# 获取CIS
def getCIS(validCircuitsList):

    cis = []

    for item in validCircuitsList:
        # 如果不是最后一个有效组件时
        if item != validCircuitsList[-1]:
            component = item.getVendorName() + ":" + item.getVendorId() + "\n" + item.getAEndPort() +  "\n" + item.getZEndPort() + "\n\n"
            cis.append(component)
        else:
            component = item.getVendorName() + ":" + item.getVendorId() + "\n" + item.getAEndPort() +  "\n" + item.getZEndPort()
            cis.append(component)

    return cis

# 获取Implementation Plan中的CIS信息
def getCISInImplementation(cis):
    cisInImplementation = ""
    for component in cis:
        cisInImplementation = cisInImplementation + component
    return cisInImplementation
