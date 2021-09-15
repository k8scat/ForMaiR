mod test {
    #[derive(Debug)]
    pub struct Person {
        name: String,
        age: u32,
    }

    pub fn new_person(name: String, age: u32) -> Person {
        Person { name, age }
    }

    impl Person {
        pub fn say(&self) {
            println!("hello world!")
        }

        pub fn get_age(&self) -> u32 {
            self.age
        }
    }
}

fn main() {
    let p = test::new_person(String::from("hsowan"), 24);
    println!("age: {}", p.get_age());
    p.say();
}
