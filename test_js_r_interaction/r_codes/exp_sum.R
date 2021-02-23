library(rjson)

## get arguments of cli
args <- commandArgs(trailingOnly = TRUE)

## arguments to JSON
json <- rjson::fromJSON(args)
a <- json$a
b <- json$b

sum <- exp(a) + exp(b);
R_version <- R.version

output <-
        list(
            a = a,
            b = b,
            exp_sum = sum,
            R_version = paste0(R_version$major, '.', R_version$minor)

        )

print(rjson::toJSON(output))
