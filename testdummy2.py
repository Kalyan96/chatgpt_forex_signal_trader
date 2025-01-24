import time

from pyChatGPT import ChatGPT

from UnlimitedGPT import ChatGPT
import xlwings as xw



def read_text_from_file(file_path, n):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if 1 <= n <= len(lines):
                return lines[n - 1].strip()
            else:
                print(f"Error: Line {n} does not exist in the file.")
                return None
    except FileNotFoundError:
        print("Error: File not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def fetch_excel_data(path, sheet_name, num_row, num_col):
    wb = xw.Book(path)
    sht = wb.sheets[sheet_name]

    # collect data
    all_values = sht.range((1, 1), (num_row, num_col)).value
    all_values[0][0] = "currency pair"
    all_values.pop(1)

    # convert 2d array into csv
    csv_values = ""
    for row in all_values:
        csv_values += ','.join(str(item) if item is not None else ' ' for item in row) + '\n'
    print(" === LOG : csv_values generated === ")
    return csv_values

def create_and_reset_chatbot(session_token, conversation_id):
    cbot = ChatGPT(session_token, conversation_id=conversation_id, proxy=None, chrome_args="", disable_moderation=False, verbose=False)
    print(" === LOG : ChatGPT Initialized === ")
    clr_string = "clear all data until now, start afresh"
    message = cbot.send_message(clr_string)
    print(" === LOG : ChatGPT Reset === ")
    return cbot


csv_values = fetch_excel_data(r"D:\networks shared drive\mt4-excel-files\openpy_tester1.xlsx", 'Sheet1', 24, 27)
print(csv_values)

#get the "__Secure-next-auth.session-token" from the inspect menu of the previouly logged in chatgpt page
session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..djFJ38Zk7G5-NHTC.lwcDdv1SCKuWFZTcZvc6qtkDATZQ5WinxM0KXmxLfs1D_ZU1YbX-WGVkYqiZKZ9GHnxuYn6WuLNxY5u4pog_6Be3vgtJChPC-Ut_YrQd1tLh6Y-AN75rzi0CtCBEHTLYGOLS7WmEtHLwvjJiQaPoFWK_WcEnJERIZyt65o5Oc13A7qGFcSfzXTGNPxIdPYgin4OcjTPLnKmhn7LYz9da-_Rz3OJe6XvmLlv-af-Md0IiJESi50xii1WzRL_H0oLtyyQULP1HKfPMBeAu5K6AQNFSoJ7jpReAuVhekU9MPFeuRZgMlP_ehFRRNJJLu244p9koDNjBGafWQbVHHAceegTq-YEd4LoVp6_Kn-ArVvkZLqkAD_VAkrFZDNaQHOTXze6a61kM0_5ooRxBdj1Kcn6KNask0O1PO6dm0HWNGsgJPGZEmRnv77D32cwS8onCQ2mv6FnYCw5L7S5NPz2SOB4ljW9TP2Kph6SjyD40mjd814G7_yiNbYMACer2RiVZTIvtYuplheY_S5SPSdYRSsW0Cy7dspoK6z38fMP9DzOfH8uMoLPOS6p587xG49w431DR3qUsKxottyuwnfg-JGXYrvlsU6Yycl8Ky9cknq23u9vMOKUouTDwH8k2emvA1ieeX7W0zyiDpXujQPbwsMzg-cZvhE5NpBAKHLIGFqlSQeBxuhhn2FC6Db1GWxuTBLZQfi9a9VCzTFD96hymRaEMVJGMrfezjHDIgwSc445kbc6a2tDVsHMjF5qWl5ELYAfFoxL1K0y5yIHaf3aW4gVoq0Lefys0WeJ0OM2rVkjYOMkby3xiccLJpIX0jJp_o2UUH0Ld6yd_VxaFu_EckYhlX6hTLkvcb_56IrP5fhhp1sblLMxADjKFX_p8RMoN9YNmRlnuCPjI462XUBk1qDfeP0n_oUrIAvBaHvI7CuSQ2F98meuq-N6VD0M8y1WvR_ox4WtelIPeW5skxuzEfQUdnga-U2D0hNXcssAa48UJx7whHxrPlnXYygYeUyKFa7-B-ZhfzgThfMoipKaAG8Rj7GyDtOqIXagDAy_uvwuRuBQRfdPkjxj-mxViV8bB6rceuMY5CfKKS7nY9LejH4egwVxNVtBWDOPnYNnJZrGCPJXy4JG6CkIiinyZ5TED1l7wN_SFRffiCBqCQuCz_2TW2d49RwPWvkshdu9jeU7vFTtQ0rss6O3plqOUT0el71PQoWV6r0ulxsKcRE-O7r5o_qBA8NJv8L0fHbzzbc4ZMS64zp3JbSEKgqJ_hln10dWfdEcNr8YH9VcNetyH8QaCPTJlTH_ou8bQPYpPtYitVVGrMiCaZMFoxAASZIDcrp95GzR7NPemPbNcPUmJMDL3Q7SNnczYmb4xBpyBU4jyUUJUIEz2r_Njrz9msQG_NLwomJKtQiKYZ0-_8e06QWhkab9HL5djAVgwad9ReM3LMfOKO84OsIcJkcOVc79iTlUCNx3bAWPB7XNxUOD1Q5YIueHfK94jv2J94krQvowEaPjSVqogEedWqetqu8Z3uLjtbuU6bdhfuFzwN-mXJv9fSbstEZ1h4C3O1jtKQYLvt-QdkszOUh0ux6zdhWIT3Pp2UyXwxHZ7hHH0oujK1v0OR5Gqww0OqX3BSN4tK-As7FLfwVdaiS80bEkC1JhYWkipurSETH1wv6C0QzM2_JEsbODBnnYC6_Yeoau-2hVgrutd-i9GRN-C1zmpIKzTLtESnDogLQnEVhWKtURhwpCl2UuawH9XT9eOMFTl7S2GH8UNy1Xlz7WRFsODqani7eEx3NXJKmMZacDQ0zNQDEKq3fxWUpWAMkBMHbkzg8C3Ym7MKYjahK8UPDhZmzLMTFrkIcYf4Csq7nJzrhcY8n2z14z6J7J-cvQCB4vXu_DwWn0jwVwC9CAyYEoOmSGkP7HbKcEIV2vHaxCwBe5Dh5fjEjNFje3U-kHLpppIYIMm9z4-48bnOJHroQEuOi4X3eDyh6E-ER_xt63M25ZCEiUxjzg2yqhHYQBHPLxvb-CotDBwFQ4gkPB7CeUJ_lTGZcqkMb9EMjzCLazIBL97Q97H0Z-cZeZSVjovArAxxpdJfBOcJyNry2cbQmQJ2OctHanXGf9HlXcXqCLKBIboctO2TzwF68MP0nmC_XDAqwPLVhZ-mo3FlqNQBW7pEW3NG41TrHWiDqObp1e6miNmInlc7vSz69p2obxOb5DgBL8Xm-MBxBznzCMn8t1lEqqpEKJTLRtfLTYP0Nd0WuAHbwoPMz0_RXeQbLZJO22R44x9zse3TYA4yXb7C_ci9cI76IXveocrvG3ivsjOTyOZ3PPzkCOQ5_XbGB3oiFhbAve7w4ghztYwiJX1B96yF3cC0asPfkONIh2LL4GZxYAIBPj4pELZMVc0f-rxsFTkjRd9abSOZQIRfsZ9a8x1BZXfOlQhtyTZ7gaNMEsxa6tvBdUr7BgplqH6Re5ySYBHIu7wD-xATcaMZfv9cnSLQ_6iw08UQEm4VU14EBBFJMBh0N-1Zy0LUg-WZVOEWPyn0x-idndgnnUJja2dC7AVyJ8GKko9sI9s9Q_fy5DEUrue5foGqOuPHZkzfsUVKN2oiN00Y0n2vFhfNtLXdIrz_3aDzIH-d8eDfODfsFYUO7EHGZVgv00yPCL0t6Rr_yl5DzqGMZt4CYUp7JQl1b85nv0-K3_Z8tKrkU5f7hyWv_lxp8X8vHgHHOFQttPe.ysPeOj4jqnsUxm-i-reZwQ'
# get the last part of URL in the chrome window after selecting any one of the previouly started chats
conversation_id = "6235a3df-57f2-46c5-8f33-9f4a8ba584e3"

chatbot = create_and_reset_chatbot(session_token,conversation_id)
#add a log message after this  line
print(" === LOG : ChatGPT Initialized === ")


# chatbot.reset_conversation()

message = chatbot.send_message(csv_values)
print(" === LOG : forex feed sent === "+time.strftime("%H:%M:%S", time.localtime()))


while True:
    # chat_message = input(":> ")
    # message = chatbot.send_message(chat_message, continue_generating=True)
    # print(message.response)
    csv_values = fetch_excel_data(r"D:\networks shared drive\mt4-excel-files\openpy_tester1.xlsx", 'Sheet1', 24, 27)
    message = chatbot.send_message(csv_values, continue_generating=True)
    resp = message.response
    print(" === LOG : sent updated  forex feed === "+time.strftime("%H:%M:%S", time.localtime()))
    message = chatbot.send_message(read_text_from_file("forex_gpt_prompt.txt",3), continue_generating=True)
    resp = message.response
    command = read_text_from_file("forex_gpt_prompt.txt",1)
    if command == "change_conv_id":
        print(" === LOG : changing conversation id === ")
        new_con_id = read_text_from_file("forex_gpt_prompt.txt", 2)
        chatbot = create_and_reset_chatbot(session_token,new_con_id)
        print(" === LOG : conversation id changed === ")
    elif command == "send_text":
        print(" === LOG : sending text === ")
        chat_message = input(":> ")
        message = chatbot.send_message(chat_message, continue_generating=True)
        print(message.response)

    time.sleep(60)


#detailed functioning of the code
#1. fetch the excel data from the excel file
#2. send the data to the chatbot
#3. get the response from the chatbot
#4. theres also conersation id change and text_send function to chatbot, for which the commands are stored in file "forex_gpt_prompt.txt"




#1. fetch the excel data from the excel file
