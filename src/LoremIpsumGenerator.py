GC_LOREM_IPSUM = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."

def lorem_ipsum_generator(p_word_count: int) -> str:
    """
    Returns a Dummy-Text with `p_word_counter`-ammount of words.
    """
    LC_LOREM_IPSUM_SPLITTED = GC_LOREM_IPSUM.split(' ')
    l_result = []
    for t_index in range(p_word_count):
        l_result.append(LC_LOREM_IPSUM_SPLITTED[t_index % 50])
    return ' '.join(l_result)
