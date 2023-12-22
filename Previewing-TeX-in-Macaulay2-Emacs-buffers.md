Using the [texfrag](https://github.com/TobiasZawada/texfrag) Emacs package, it is possible to preview TeX code in Macaulay2 interaction buffers in a way similar to the `preview-latex` mode that comes with [AUCTeX](https://www.gnu.org/software/auctex/).

After installing texfrag (which is available through [MELPA](https://melpa.org/)), add the following to your `.emacs` or `.init.el`:

```elisp
(require 'texfrag)

(defun texfrag-M2-comint ()
  "Texfrag setup for `M2-comint-mode'."
  (when texfrag-mode
	(setq texfrag-comments-only nil
	      texfrag-frag-alist '(("\\$" "\\$" "$" "$")))))

(push (list #'texfrag-M2-comint #'M2-comint-mode) texfrag-setup-alist)
```

Then, when in an M2 interaction window buffer, start texfrag using <kbd>M</kbd>-<kbd>x</kbd> `texfrag-mode`.  Alternatively, you can set texfrag to start automatically in Macaulay2 interaction buffers by adding the following to your configuration:

```elisp
(add-hook 'M2-comint-mode-hook #'texfrag-mode)
```

As an example, consider the following session:

![image](https://github.com/Macaulay2/M2/assets/1992248/419e2af9-6482-4331-86ce-ca6f324afc31)

Now suppose we run <kbd>M</kbd>-<kbd>x</kbd> `preview-at-point` (or its key binding, <kbd>C</kbd>-<kbd>c</kbd> <kbd>C</kbd>-<kbd>p</kbd> <kbd>C</kbd>-<kbd>p</kbd>).  Then we get the following:

![image](https://github.com/Macaulay2/M2/assets/1992248/94ac87ff-53d2-46e9-8f9c-2096d864e0ef)
