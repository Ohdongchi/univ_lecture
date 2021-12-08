import dpkt
import socket
import binascii
with open('test.pcap', 'rb') as f:
##    print(bytes.fromhex(f.read()))
    pcap = dpkt.pcap.Reader(f)  # file 불러옴
    dic = {}
    imgString=[]
    cnt =0
    finish=''
    cookie=''
    for timestamp, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        
        ip = eth.data
        
        if eth.type != dpkt.ethernet.ETH_TYPE_IP:
            continue
        if ip.p != dpkt.ip.IP_PROTO_TCP:
            continue

        tcp = ip.data

        if len(str(tcp.data.hex())) < 10:
            continue

        streamIndex = socket.inet_ntoa(ip.src) + ':' + str(tcp.sport) + ':'
        streamIndex += socket.inet_ntoa(ip.dst) + ':' + str(tcp.dport) + ':' + str(tcp.ack)
        
        # seq= 11111
        # seq1= 11111:data
        # seq2= 11111:data
        # 아래 코드 설명
        # 시퀀스를 설정하고 기존에 시퀀스가 존재한다면 그 시퀀스의 데이터 뒤에 분할된 데이터를 이어 붙히고
        # 시퀀스가 존재하지 않다면 새로 추가한다.
        
        if streamIndex in dic:  # 시퀀스가 맞은 데이터끼리 찾아서 시퀀스를 뺀 나머지 데이터들을 조합하면 원본데이터
            streamIndexValue = dic[streamIndex]
            streamIndexValue += ':' + str(tcp.seq) + ',' + str(tcp.data.hex())
            del dic[streamIndex]
            dic[streamIndex] = streamIndexValue
        else:
            dic[streamIndex] = str(tcp.seq) + ',' + str(tcp.data.hex())
    
    for key in dic:

        streamValue1 = dic[key]
        arr1 = streamValue1.split(':')
        strSeq = []
        strData = []
        for val in arr1:
            arr2 = val.split(',')
            strSeq.append(arr2[0])
            strData.append(arr2[1])
            
      #정렬
        #같은 데이터 즉 같은 키값끼리 정렬하여 나열한다.오름차
        for i in range(len(strSeq)):
            for j in range(len(strSeq) - 1):
                sseq = int(strSeq[j + 1])
                sdata = strData[j + 1]
                if int(strSeq[j]) > int(strSeq[j + 1]):
                    del strSeq[j + 1]
                    strSeq.insert(j, sseq)
                    del strData[j + 1]
                    strData.insert(j, sdata)

        allpacket = ''
        for packet in strData: # 이미지 한개의 데이터 hex값들 
            allpacket += packet

        result1 = allpacket.find('ffd8ffe0')
        result2 = ["ff","d9"]
##        for i in range(len(allpacket)):
        
        result2 = allpacket.rfind('ffd9')
        
        #이미지 파일 패킷만 가져오기 
        if result1 > -1 and result2 > -1:
            imgString = allpacket[result1:result2+4]

            # 밑에 if문을 사용한 이유
            # if문을 사용한 이유는 이렇습니다. 만약에 이미지패킷의 길이가 홀수면
            # hex-decimal이 홀수임으로
            # wb 즉 binary write가 불가능합니다.
            # 그래서 홀수일 때는 넘기고 짝수 일 때만 실행하게 해야합니다.
            if (len(imgString)%2==0): 
                with open(str(cnt)+".jpg","wb") as file:
                    file.write(bytes.fromhex(imgString))
                    cnt+=1
    print("끝")
