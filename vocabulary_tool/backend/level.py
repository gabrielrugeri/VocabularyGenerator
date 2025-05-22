class Difficulty:
    d = {
        1: ('beginner', 'iniciante'),
        2: ('intermediate', 'intermediário'),
        3: ('advanced', 'avançado'),
    }
    
    @classmethod
    def get_level(cls, level: int, language: str = 'en') -> str:
        """Retorna o termo de dificuldade no idioma especificado"""
        if level not in cls.d:
            raise ValueError(f"Nível inválido. Opções: {list(cls.d.keys())}")
        if language == 'en':
            return cls.d[level][0]
        elif language == 'pt':
            return cls.d[level][1]
        else:
            raise ValueError("Invalid language. Use 'en' or 'pt'")
    
    @classmethod
    def get_level_number(cls, term: str) -> int:
        """Retorna o número do nível com base no termo (em qualquer idioma)"""
        term_lower = term.lower()
        for level, (en, pt) in cls.d.items():
            if term_lower in (en, pt):
                return level
        raise ValueError(f"Termo de dificuldade inválido. Opções: {cls.get_all_terms()}")
    
    @classmethod
    def get_all_terms(cls) -> list:
        """Retorna todos os termos de dificuldade em ambos os idiomas"""
        terms = []
        for en, pt in cls.d.values():
            terms.extend([en, pt])
        return terms
    
    @classmethod
    def translate(cls, term: str, target_language: str = 'en') -> str:
        """Traduz um termo de dificuldade para o idioma alvo"""
        level = cls.get_level_number(term)
        return cls.get_level(level, target_language)

# Exemplos de uso:
# Difficulty.get_level(1, 'pt'))  # Output: facil
# Difficulty.get_level_number('medio'))  # Output: 2
# Difficulty.translate('hard', 'pt'))  # Output: dificil
# Difficulty.translate('facil', 'en'))  # Output: easy