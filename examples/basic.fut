entry main : [256][512][3]u8 =
  map (\y ->
         (map (\x ->
                 [u8.i32 (x / 2), u8.i32 y, 0])
              (iota 512)))
      (iota 256)
