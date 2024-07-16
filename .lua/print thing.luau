-- there might be errors in here

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