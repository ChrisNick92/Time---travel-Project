import time
import sys
import lib

N = int(sys.argv[1]) # total moves

if N <= 1000:
    tic = time.time()
    try:
        input = sys.argv[2]
    except:
        input = "DEFAULT"
    default_companies = True
    if len(sys.argv) == 2 or len(sys.argv) == 4:# Default Companies
        companies = {'GE', 'AMZN', 'AAPL'}
    elif input == "COMPANIES": # Companies inserted by the User
        M = int(sys.argv[3]) # Number of Companies
        companies = set([sys.argv[i] for i in range(4, M+4)])
        default_companies = False
    else:
        print("Error! Check your input again!")
        
    # Trading starts here   
    portfolio = lib.initialize_portfolio(companies)
    time_traveler = lib.tracking(portfolio)
    time_traveler = lib.trading_loop(time_travel = time_traveler, companies = companies,
                     N = N, sales_margin = 2, life_span_factor_sell = 0.3,
                     life_span_factor_buy = 0.3, intra_days = 20,
                     early_buy_factor = 1, late_buy_factor = 0.98, early_sell_factor = 1.1,
                     early_sell_volume = 0.5, late_sell_factor = 1.2, late_sell_volume = 0.7,
                     intra_day_factor = 0.3)
    time_traveler.portfolio_plot()
    
    # Print the results
    print("\n\n ----> The Time Travel Project 2022 <----\n")

    # Print the transactions or(exclusive) save the txt file ?
    if (len(sys.argv)>3 and sys.argv[2] == "PRINT" and sys.argv[3] == "TRUE") or \
       (input == "COMPANIES" and len(sys.argv) == 6+M and sys.argv[4+M] == "PRINT" and\
        sys.argv[5+M] == "TRUE"):
        print("\n----> List of transactions <----\n")
        for x in time_traveler.moves:
            print(str(x[0].strftime("%Y-%m-%d")) + ' ' + x[1] + ' ' + x[2] + ' ' + str(x[3]))
        print("\n")
    elif (len(sys.argv)>3 and sys.argv[2] == "SAVEFILE" and sys.argv[3] == "TRUE") or\
         (input == "COMPANIES" and len(sys.argv) == 6+M and sys.argv[4+M] == "SAVEFILE" and\
          sys.argv[5+M] == "TRUE"):
        lib.convert_to_txt(time_traveler.moves, "small.txt")
        
    # Summary of transactions
    print("Summary of results:")
    print("- Upper bound of total transactions: ", N)
    print(f"- Default Companies: ", companies) if default_companies\
       else print(f"- Your Companies: ", companies)
    print("- Total transactions: ", len(time_traveler.moves))
    print("- Money earned: ", time_traveler.money)
    print("\nRun time: ", lib.timer(time.time()-tic))
    
elif N > 1000:
    tic = time.time()
    try:
        input = sys.argv[2]
    except:
        input = "DEFAULT"
    default_companies = True
    if len(sys.argv) == 2 or len(sys.argv) == 4:# Default Companies
        companies = {'CSCO', 'MO', 'SIRI', 'HD', 'FB', 'ORCL', 'AAPL',
                 'EBAY', 'MSFT', 'GE','INTC', 'BAC'}
    elif input == "COMPANIES": # Companies inserted by the User
        M = int(sys.argv[3]) # Number of Companies
        companies = set([sys.argv[i] for i in range(4, M+4)])
        default_companies = False
    else:
        print("Error! Check your input again!")
    
    # Trading starts here    
    portfolio = lib.initialize_portfolio(companies)
    time_traveler = lib.tracking(portfolio)
    time_traveler = lib.trading_loop(time_travel = time_traveler, companies = companies,
                     N = N, sales_margin = 2, life_span_factor_sell = 0.95,
                     life_span_factor_buy = 0.3, intra_days = 700,
                     early_buy_factor = 1.4, late_buy_factor = 0.98, early_sell_factor = 1,
                     early_sell_volume = 0.3, late_sell_factor = 1.4, late_sell_volume = 0.7,
                     intra_day_factor = 1e-7)
    time_traveler.portfolio_plot()

    # Print the results
    print("\n\n ----> The Time Travel Project 2022 <----\n")

    # Print the transactions or(exclusive) save the txt file ?
    if (len(sys.argv)>3 and sys.argv[2] == "PRINT" and sys.argv[3] == "TRUE") or \
       (input == "COMPANIES" and len(sys.argv) == 6+M and sys.argv[4+M] == "PRINT" and\
        sys.argv[5+M] == "TRUE"):
        print("\n----> List of transactions <----\n")
        for x in time_traveler.moves:
            print(str(x[0].strftime("%Y-%m-%d")) + ' ' + x[1] + ' ' + x[2] + ' ' + str(x[3]))
        print("\n")
    elif (len(sys.argv)>3 and sys.argv[2] == "SAVEFILE" and sys.argv[3] == "TRUE") or\
         (input == "COMPANIES" and len(sys.argv)==6+M and sys.argv[4+M] == "SAVEFILE" and\
          sys.argv[5+M] == "TRUE"):
        lib.convert_to_txt(time_traveler.moves, "large.txt")
        
    # Summary of transactions
    print("Summary of results:")
    print("- Upper bound of total transactions: ", N)
    print(f"- Default Companies: ", companies) if default_companies\
        else print(f"- Your Companies: ", companies)   
    print("- Total transactions: ", len(time_traveler.moves))
    print("- Money earned: ", time_traveler.money)
    print("\nRun time: ", lib.timer(time.time()-tic))


    
