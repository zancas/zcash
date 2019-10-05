use std::fs::File;

fn main() -> std::io::Result<()> {
    use std::env;
    use std::io::Read;
    let filename = format!(
        "{}/imageid.txt",
        env::current_dir().unwrap().parent().unwrap().display()
    );
    let mut contents = String::new();
    File::open(filename)
        .unwrap()
        .read_to_string(&mut contents)?;
    let index = contents.rmatch_indices("ami-").collect::<Vec<_>>()[0].0;
    let image_name = contents.split_at(index).1.trim();
    println!("{:?}", image_name);
    Ok(())
}
