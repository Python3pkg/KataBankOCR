"data about input_files used for testing"

class Basic:
    "details regarding the Basic input file"

    path = 'parser/test/input_files/basic.txt'
    line_count = 44
    accounts = ['000000000', '111111111', '222222222', '333333333', '444444444', '555555555',
                '666666666', '777777777', '888888888', '999999999', '123456789']
    valid_accounts = ['000000000', '123456789']
    invalid_accounts = ['111111111', '222222222', '333333333', '444444444', '555555555',
                        '666666666', '777777777', '888888888', '999999999']
    story_three_results = ['000000000', '111111111 ERR', '222222222 ERR', '333333333 ERR',
                           '444444444 ERR', '555555555 ERR', '666666666 ERR', '777777777 ERR',
                           '888888888 ERR', '999999999 ERR', '123456789',]
    story_four_results = ['000000000', '111111111 ERR', '222222222 ERR', '333333333 ERR',
                          '444444444 ERR', '555555555 AMB', '666666666 AMB', '777777177',
                          '888888888 AMB', '999999999 AMB', '123456789']

class Advanced:
    "details regarding the Advanced input file"

    path = 'parser/test/input_files/advanced.txt'
    line_count = 32
    story_three_results = ['000000051', '49006771? ILL', '1234?678? ILL', '200000000 ERR',
                           '490067715 ERR', '?23456789 ILL', '0?0000051 ILL', '49086771? ILL']

    story_four_results = ['000000051', '490067715 AMB', '1234?678?', '200000000',
                        '490067715 AMB', '123456789', '000000051', '490867715']
