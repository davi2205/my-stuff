#[derive(Debug)]
struct Tijolo {
    x: i32,
    y: i32,
    largura: i32,
    altura: i32,
    vida: i32,
}

fn main() {
    let tela_largura = 640;
    let tela_altura = 480;

    let tijolos: Box<[Tijolo]> = {
        let mut cursor_x = 5;
        let mut cursor_y = 10;
        let tijolo_altura = 20;

        let mut tijolos = Vec::new();

        let mapa = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 6, 6, 6, 6, 6, 6, 6, 0],
            [0, 5, 5, 5, 5, 5, 5, 5, 0],
            [0, 4, 4, 4, 4, 4, 4, 4, 0],
            [0, 3, 3, 3, 3, 3, 3, 3, 0],
            [0, 2, 2, 2, 2, 2, 2, 2, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0],
        ];

        for linha in mapa.iter() {
            let tijolo_largura = (tela_largura + 5) / linha.len() as i32;

            for &vida_tijolo in linha {
                if vida_tijolo > 0 {
                    let tijolo = Tijolo {
                        x: cursor_x,
                        y: cursor_y,
                        largura: tijolo_largura - 5,
                        altura: tijolo_altura,
                        vida: vida_tijolo,
                    };

                    tijolos.push(tijolo);
                }

                cursor_x += tijolo_largura;
            }

            cursor_x = 5;
            cursor_y += tijolo_altura + 5;
        }

        tijolos.into()
    };

    dbg!(tijolos);

    println!("Hello, world!");
}
