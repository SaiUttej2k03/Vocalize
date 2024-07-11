defgetText():  #This function links the VSCODE with the awsmanagagement console
    aws_mg_con=boto3.session.Session(profile_name='Demo_user')  #To access management console using the IAM User created ieDemo_user
    client1=aws_mg_con.client(service_name='polly',region_name='us-east-1')
     
    result=textEx.get("1.0","end")
    print(result)
    response=client1.synthesize_speech(VoiceId='Emma',OutputFormat='mp3',Text=result,Engine='neural')  #Synthesize_speech is the module in polly which deals with voices
    print(response)
    if"AudioStream"in response:
        with closing(response['AudioStream'])as stream:
            output=os.path.join(gettempdir(),"This_is_The_output.mp3")  #If the AudioStream is present in the dictionary printed in the output, then Windows media player 
            #and gives the output of the text entered by the user as file 'This_is_The_output
            try:
                withopen(output,"wb")asfile:
                    file.write(stream.read())
            exceptIOErroras error:
                print(error)
                sys.exit(-1)
                #If there is any error we use exception handling to avoid abnormal termination of program

    else:
        print("Could not find the stream")
        sys.exit(-1)

    ifsys.platform=='win32':
        os.startfile(output)  #System identifies the platform and executes the output

btnread=tk.Button(root,height=1,width=10,text="Read",command=getText)
btnread.pack()
#The above creates  a button called 'Read' 

root.mainloop()
#Closes the GUI only after you press the cross symbol [X]
