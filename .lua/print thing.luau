-- there will be some errors in here (this works in roblox i tested)

local function print()
    local yes = "haha yes"
    local no = "nuh uh uh"
    task.wait(3)
---@diagnostic disable-next-line: redundant-parameter
    print(yes)
    task.wait(3)
---@diagnostic disable-next-line: redundant-parameter
    print(no)
end