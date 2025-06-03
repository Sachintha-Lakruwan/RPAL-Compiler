class ControlStructureGenerator:
    def __init__(self):
        self.deltas = {}
        self.delta_counter = 0

    def generate(self, node):
        # the very first control‐structure is called delta0
        control_struct = self._traverse(node)
        self.deltas["delta0"] = control_struct
        return self.deltas

    def _traverse(self, node):
        result = []

        # ─── handle lambda as before ───
        if node.value == "lambda":
            delta_name = f"delta{self.delta_counter + 1}"
            lam_name   = f"lambda{self.delta_counter + 1}"
            var        = node.children[0].value
            body       = node.children[1]

            self.delta_counter += 1
            # build the body‐structure as its own delta
            body_struct = self._traverse(body)
            self.deltas[delta_name] = body_struct

            result.append(f"{lam_name}{var}")

        # ─── NEW: handle conditional (->) ───
        elif node.value == "->":
            # children: [cond, true_branch, false_branch]
            cond_node, true_node, false_node = node.children

            # allocate two new deltas
            delta_true  = f"delta{self.delta_counter + 1}"
            delta_false = f"delta{self.delta_counter + 2}"
            self.delta_counter += 2

            # emit them, then 'beta', then the flattened condition
            result.extend([delta_true, delta_false, "beta"])
            result.extend(self._traverse(cond_node))

            # build each branch into its own delta
            self.deltas[delta_true]  = self._traverse(true_node)
            self.deltas[delta_false] = self._traverse(false_node)

        # ─── everything else ───
        else:
            result.append(node.value)
            for child in node.children:
                result.extend(self._traverse(child))

        return result