grep ", loss = " log.01accu | awk '{print ($(NF-3))" "$NF}' | sed 's/,//g' > loss
