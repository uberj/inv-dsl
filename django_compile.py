def compile_Q(stack):
    q_stack = []
    while True:
        try:
            top = stack.pop()
        except IndexError:
            break
        if (istype(top, 'TERM') or istype(top, 'DIRECTIVE') or
                istype(top, 'RE'):
            q_stack.append(top.compile_Q())
        elif istype(top, 'NOT'):
            term = q_stack.pop()
            q_stack.append(lambda Q: ~Q, term)
            continue
        elif istype(top, 'AND') or istype(top, 'OR'):
            t1 = q_stack.pop()
            t2 = q_stack.pop()
            q_result = []
            for qi, qj in izip(t1, t2):
                if istype(top, 'AND'):
                    if qi and qj:
                        q_result.append(qi & qj)
                    else: # Something AND nothing is nothing
                        q_result.append(None)
                elif istype(top, 'OR'):
                    if qi and qj:
                        q_result.append(qi | qj)
                    elif qi:
                        q_result.append(qi)
                    elif qj:
                        q_result.append(qj)
                    else:
                        q_result.append(None)
            q_stack.append(q_result)
    return q_stack
