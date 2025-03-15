export class RecintosZoo {
    constructor() {
        this.recintos = [
            { numero: 1, bioma: "savana", tamanhoTotal: 10, animais: [{ especie: "MACACO", quantidade: 3 }] },
            { numero: 2, bioma: "floresta", tamanhoTotal: 5, animais: [] },
            { numero: 3, bioma: "savana e rio", tamanhoTotal: 7, animais: [{ especie: "GAZELA", quantidade: 1 }] },
            { numero: 4, bioma: "rio", tamanhoTotal: 8, animais: [] },
            { numero: 5, bioma: "savana", tamanhoTotal: 9, animais: [{ especie: "LEAO", quantidade: 1 }] }
        ];

        this.animaisPermitidos = {
            LEAO: { tamanho: 3, biomas: ["savana"], carnivoro: true },
            LEOPARDO: { tamanho: 2, biomas: ["savana"], carnivoro: true },
            CROCODILO: { tamanho: 3, biomas: ["rio"], carnivoro: true },
            MACACO: { tamanho: 1, biomas: ["savana", "floresta"], carnivoro: false },
            GAZELA: { tamanho: 2, biomas: ["savana"], carnivoro: false },
            HIPOPOTAMO: { tamanho: 4, biomas: ["savana", "rio"], carnivoro: false }
        };
    }

    analisaRecintos(animal, quantidade) {
        const erro = this.validaEntrada(animal, quantidade);
        if (erro) return { erro };

        const recintosViaveis = this.recintos
            .filter(recinto => this.isRecintoViavel(recinto, animal, quantidade))
            .map(recinto => this.formataRecinto(recinto, animal, quantidade));

        return recintosViaveis.length > 0 
            ? { recintosViaveis } 
            : { erro: "Não há recinto viável" };
    }

    validaEntrada(animal, quantidade) {
        if (!this.animaisPermitidos[animal]) return "Animal inválido";
        if (quantidade <= 0) return "Quantidade inválida";
        return null;
    }

    isRecintoViavel(recinto, animal, quantidade) {
        const especie = this.animaisPermitidos[animal];
        if (!especie.biomas.includes(recinto.bioma)) return false;

        const espacoOcupado = this.calculaEspacoOcupado(recinto);
        const espacoNecessario = this.calculaEspacoNecessario(recinto, animal, quantidade);

        return espacoNecessario <= recinto.tamanhoTotal - espacoOcupado;
    }

    calculaEspacoOcupado(recinto) {
        return recinto.animais.reduce((total, animal) => {
            const especie = this.animaisPermitidos[animal.especie];
            return total + (especie.tamanho * animal.quantidade);
        }, 0);
    }

    calculaEspacoNecessario(recinto, novoAnimal, quantidade) {
        const especie = this.animaisPermitidos[novoAnimal];
        let espacoNecessario = especie.tamanho * quantidade;

        if (recinto.animais.length > 0) espacoNecessario += 1;

        return espacoNecessario;
    }

    formataRecinto(recinto, animal, quantidade) {
        const espacoLivre = recinto.tamanhoTotal - this.calculaEspacoOcupado(recinto) - this.calculaEspacoNecessario(recinto, animal, quantidade);
        return `Recinto ${recinto.numero} (espaço livre: ${espacoLivre} total: ${recinto.tamanhoTotal})`;
    }
}
