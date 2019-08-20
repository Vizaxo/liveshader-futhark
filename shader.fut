let shader (x: i32) (y: i32) : [3]u8 = [u8.i32 x, u8.i32 (y / 2), 0]

entry main (time: f32) : [256][512][3]u8 =
  map (\x -> (map (shader x) (iota 512))) (iota 256)
