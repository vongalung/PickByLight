from pyModbusTCP.client import ModbusClient
from pyModbusTCP.constants import MODBUS_RTU
from config.modbus import *
from time import sleep
    
### MODBUS INITIALIZATION
c = ModbusClient()
c.mode(MODBUS_RTU) # enable MODBUS_RTU mode
c.timeout(1)
c.debug(True)
c.auto_open(True)
c.auto_close(True)

reg_value={'dum':None} # DUMMY FOR RECORDING REGISTRY LISTS
### END MODBUS INITIALIZATION

### INTERNAL FUNCTIONS
def loc_id(loc):
    device=loc.split('.')
    modmap,conn_id = MODBUS_MAP[device[2]],CONNECTIONS[device[0]][device[1]]
    return modmap,conn_id # [slave_id,reg_values],[IP_addr,port,slave_id_modifier]

def reg_add(modmap,color):
    reg=[0x0,0x0,0x0]
    for cl in COLOR_LIST[color]:
        mapcol=modmap[1][cl] # [0xXXXX,0xXXXX,0xXXXX]
        for i in range(0,3):
            reg[i]+=mapcol[i]
    return reg

def open_comm(): # MODBUS AUTO-RECONNECT
    while not c.is_open():
        c.open()
        sleep(0.1)

## MODBUS READ (FOR CORRECTION)
def read_reg():
    dum=None
    cnt=0
    while dum is None:
        if cnt < 3:
            dum = c.read_holding_registers(4,3)
            sleep(0.2)
            cnt+=1
        else:
            dum=[0x0,0x0,0x0]
            break
    return dum
## END MODBUS READ

### END INTERNAL FUNCTIONS

### WRITE TO MODBUS        
def modbus_comm(ip='localhost',port=5000,regdict=[None],color='1'):
    ## CREATE CONNECTION TO IP=ip:port
    c.host(ip)
    c.port(port)
    open_comm()
    ## END CREATE CONNECTION
    
    response='[IP: /%s]\n' %ip
    for slave in regdict:
        # Modbus writing is done by comparing current registries status with the registries from regdict.
        # If color=='1' (LAMP OFF), filter out the regdict regitries from the current registries status;
        # otherwise, simply add the regdict registries into the current one.
        c.unit_id(slave)    # assign device/slave_id number
        curr_reg = read_reg() # read current registries status
        sleep(0.2)
        wrt_reg=[0x0,0x0,0x0]
        if color == '1': # LAMP OFF
            dum=[0xffff,0xffff,0xffff]
            flt_reg=[0x0,0x0,0x0]
            for i in range(0,3):
                flt_reg[i]=dum[i]^regdict[slave][i]
                wrt_reg[i]=curr_reg[i]&flt_reg[i] # filtering out (w/ bitwise binary 'AND' operator)
        else: # LAMP ON
            for i in range(0,3):
                wrt_reg[i]=curr_reg[i]|regdict[slave][i] # add registries status (w/ bitwise binary 'OR' operator)
        c.write_multiple_registers(4, wrt_reg) # write status changes over modbus
        sleep(0.2)
        
        ## RISK MANAGEMENT
        # In the event that not all values are written down correctly,
        # repeat sending registry values
        curr_reg = read_reg()
        sleep(0.2)
        cnt=0
        while not (curr_reg == wrt_reg):
            if cnt < 3: # try up to 3 attempts before reporting failure
                cnt+=1
                c.write_multiple_registers(4, wrt_reg)
                sleep(0.2)
                curr_reg = read_reg()
                sleep(0.2)
            else:
                response+='Failed at address : %s\n' % str(slave)
                break
        ## END RISK MANAGEMENT
        
    c.close()
    return response
### END WRITE TO MODBUS

### MAIN EXECUTION CODE    
def execute(loc_list,color):
    global reg_value # reg_value will consists of:
                     # {
                     #   ip_1:[
                     #     port,
                     #     {
                     #        slv_1:[0xX,0xX,0xX],
                     #        slv_2:[0xX,0xX,0xX],
                     #        .... (next_slv)
                     #     }
                     #   ],
                     #   ip_2:[
                     #     port,
                     #     {
                     #        slv_1:[0xX,0xX,0xX],
                     #        slv_2:[0xX,0xX,0xX],
                     #        .... (next_slv)
                     #     }
                     #   ],
                     #   .... (next_ip)
                     # }
    
    reg_value={'dum':None}
    response=''
    for l in loc_list:
        modmap,conn_id=loc_id(l) # [slave_id,reg_values],[IP_addr,port,slave_id_modifier]
        slv_id=modmap[0]+conn_id[2]
        dum=reg_add(modmap,color) # [0xXXXX,0xXXXX,0xXXXX]
        
        if conn_id[0] in reg_value:
            if slv_id in reg_value[conn_id[0]]:
                # if entry for this ip and slv_id exists, add the value into it
                for i in range(0,3):
                    reg_value[conn_id[0]][1][slv_id][i]+=dum[i]
            else:
                # if entry for this slv_id is not exist on this ip, create new slv_id entry
                reg_value[conn_id[0]][1][slv_id]=dum
        else:
            # if entry for this ip is not exist, create new entry for this ip and slv_id
            reg_value[conn_id[0]]=[conn_id[1]]
            reg_value[conn_id[0]]+=[{slv_id:dum}]
            
    del reg_value['dum'] # remove the dummy initial value
    for ip in reg_value:
        # write to modbus for each ip entries
        response+=modbus_comm(ip,reg_value[ip][0],reg_value[ip][1],color)
    return response

### END MAIN EXECUTION CODE
    

