# Automatic preview
Automatic preview means that whenever the output is a latex fragment, it will automatically be compiled and rendered.  For example:

<img alt="image" src="https://github.com/user-attachments/assets/6cd29170-753d-41d1-9487-ef3328ac207f" />

To enable this feature, copy the emacs code below to your `.enacs` or `init.el`.  Note that it requires 

1. The `texfrag` Emacs package, which is for example installable in Emacs via `M-x package-install RET texfrag`.  If you are unsure whether `texfrag` is already installed, run `M-x list-packages` and check the installed packages listed at the very bottom.
2. A functioning `auctex` setup in Emacs, meaning you can compile latex documents with Emacs.
2. The `dvipng` system executable, which is for example installable via:
     - on Debian / Ubuntu: `sudo apt install dvipng`
     - on Fedora: `sudo dnf install texlive-dvipng`
     - on MacOS:  `dvipng` is bundled with most TeX distributions
   
   If you are unsure whether `dvipng` is already installed, run `dvipng --version` in your terminal and check the output.

```elisp
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Automatic LaTeX Rendering for Macaulay2 Buffers
;; Requires: 'texfrag' package (M-x package-install RET texfrag)
;;           'dvipng' system executable
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(with-eval-after-load 'M2  ; Change 'M2 to your package's actual feature name if needed

  (defun M2--texfrag-standalone-header ()
    "Generate a wide article LaTeX preamble for Macaulay2 latex fragments."
    (concat
     "\\documentclass{article}\n"
     "\\setlength{\\textwidth}{10000pt}\n"
     "\\usepackage{amsmath,amsfonts}\n"
     "\\usepackage[utf8]{inputenc}\n"
     "\\usepackage[T1]{fontenc}\n"))

  (defun M2--texfrag-comint ()
    "Internal texfrag setup for `M2-comint-mode'."
    (when (bound-and-true-p texfrag-mode)
      (setq-local texfrag-comments-only nil)
      (setq-local texfrag-frag-alist '(("\\$" "\\$" "$" "$")))
      (setq-local texfrag-header-function #'M2--texfrag-standalone-header)))

  (defmacro M2--with-texfrag-preview-settings (&rest body)
    "Execute BODY with AUCTeX preview settings strictly bound to DVI/PNG."
    `(let ((preview-image-type 'dvi*)
           (preview-dvi*-image-type 'png)
           (preview-LaTeX-command-replacements '(preview-LaTeX-disable-pdfoutput))
           (preview-dvipng-command "dvipng -picky -noghostscript -o %m/prev%%03d.png %d")
           (TeX-PDF-mode nil)
           (TeX-master t))
       ,@body))

  (defun M2--texfrag-auto-render-output (_string)
    "Scan newly arrived comint output line-by-line and compile LaTeX fragments."
    (when (and (bound-and-true-p texfrag-mode)
               (boundp 'comint-last-output-start)
               comint-last-output-start)
      (let ((start comint-last-output-start)
            (end (point-max)))
        (save-excursion
          (goto-char start)
          (while (re-search-forward "^[ \t]*o[0-9]+[ \t]*=[ \t]*\\$\\(?:.\\|\n\\)*?\\$[ \t]*$" end t)
            (let ((match-start (match-beginning 0))
                  (match-end (match-end 0)))
              (M2--with-texfrag-preview-settings
               (if (fboundp 'texfrag-region)
                   (texfrag-region match-start match-end)
                 (when (fboundp 'preview-region)
                   (preview-region match-start match-end))))))))))

  (define-minor-mode M2-texfrag-auto-mode
    "Minor mode to auto-compile and preview LaTeX fragments in Macaulay2 shells."
    :init-value nil
    :lighter " M2-LaTeX"
    (if M2-texfrag-auto-mode
        (cond
         ((not (require 'texfrag nil t))
          (setq M2-texfrag-auto-mode nil)
          (user-error "Package 'texfrag' is required. Please run: M-x package-install RET texfrag"))
         ((not (executable-find "dvipng"))
          (setq M2-texfrag-auto-mode nil)
          (user-error "Executable 'dvipng' not found on your system PATH"))
         (t
          (when (boundp 'texfrag-setup-alist)
            (add-to-list 'texfrag-setup-alist (list #'M2--texfrag-comint #'M2-comint-mode)))
          (unless (bound-and-true-p texfrag-mode)
            (texfrag-mode 1))
          (add-hook 'comint-output-filter-functions #'M2--texfrag-auto-render-output nil t)
          (M2--with-texfrag-preview-settings
           (if (fboundp 'texfrag-document)
               (texfrag-document)
             (when (fboundp 'preview-buffer)
               (preview-buffer))))))
      (remove-hook 'comint-output-filter-functions #'M2--texfrag-auto-render-output t)
      (when (fboundp 'preview-clearout-buffer)
        (preview-clearout-buffer))))

  ;; Automatically activate the mode whenever a Macaulay2 shell buffer starts
  (add-hook 'M2-comint-mode-hook #'M2-texfrag-auto-mode))
```

# Manual preview

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
