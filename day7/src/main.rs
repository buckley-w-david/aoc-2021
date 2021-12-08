use std::fs::read_to_string;

trait Fuel {
    fn linear_fuel(&self, target: &i32) -> u32;
    fn gauss_fuel(&self, target: &i32) -> u32;
}

impl Fuel for i32 {
    fn linear_fuel(&self, target: &i32) -> u32 {
        i32::abs(self - target) as u32
    }

    fn gauss_fuel(&self, target: &i32) -> u32 {
        let dist = i32::abs(self - target) as u32;
        ((dist)*(dist+1))/2
    }
}


fn part_one(positions: &Vec<i32>) -> u32 {
    let min = *positions.iter().min().unwrap();
    let max = *positions.iter().max().unwrap();
    let fuels: Vec<u32> = (min..max).map(|target| positions.iter().map(move |pos| pos.linear_fuel(&target)).sum()).collect();
    *fuels.iter().min().unwrap()
}

fn part_two(positions: &Vec<i32>) -> u32 {
    let min = *positions.iter().min().unwrap();
    let max = *positions.iter().max().unwrap();
    let fuels: Vec<u32> = (min..max).map(|target| positions.iter().map(move |pos| pos.gauss_fuel(&target)).sum()).collect();
    *fuels.iter().min().unwrap()
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let positions = read_to_string("input")?.trim().split(",").map(|i| i.parse().unwrap()).collect();
    println!("Part 1: {}", part_one(&positions));
    println!("Part 2: {}", part_two(&positions));

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn example_data() -> Vec<i32> {
        vec![16,1,2,0,4,2,7,1,2,14]
    }

    #[test]
    fn test_part_one() {
        let input = example_data();
        let res = part_one(&input);
        assert_eq!(res, 37);
    }

    #[test]
    fn test_part_two() {
        let input = example_data();
        let res = part_two(&input);
        assert_eq!(res, 168);
    }
}
