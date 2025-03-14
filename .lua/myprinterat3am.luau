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

-- printer idk what it does i forgot what it does it just prints yes after 3 sec and then no after 3 sec then dies 😎